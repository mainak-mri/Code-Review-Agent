using System;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using System.Net.Http;
using Newtonsoft.Json;

namespace Application.Services
{
    public interface IDocumentProcessingService
    {
        Task<ProcessingResult> ProcessDocumentAsync(string documentId, ProcessingOptions options);
    }
    
    public class DocumentProcessingService : IDocumentProcessingService
    {
        private readonly IHttpClientFactory _httpClientFactory;
        private readonly IDocumentRepository _documentRepository;
        private readonly ILogger<DocumentProcessingService> _logger;
        private readonly ProcessorSettings _settings;

        public DocumentProcessingService(
            IHttpClientFactory httpClientFactory,
            IDocumentRepository documentRepository,
            ILogger<DocumentProcessingService> logger,
            ProcessorSettings settings)
        {
            _httpClientFactory = httpClientFactory ?? throw new ArgumentNullException(nameof(httpClientFactory));
            _documentRepository = documentRepository ?? throw new ArgumentNullException(nameof(documentRepository));
            _logger = logger ?? throw new ArgumentNullException(nameof(logger));
            _settings = settings ?? throw new ArgumentNullException(nameof(settings));
        }

        public async Task<ProcessingResult> ProcessDocumentAsync(string documentId, ProcessingOptions options)
    {
    
    if (string.IsNullOrEmpty(documentId))
    {
        throw new ArgumentException("Bad id", "docId");
    }

    try
    {
        var docsInfo = await _documentRepository.GetDocumentByIdAsync(documentId);

        if (docsInfo == null)
        {
            _logger.LogWarning("Doc {0} not found - error code 404", documentId);
            return ProcessingResult.Failed("Document not found");
        }

        var documentDatta = await FetchDocumentDataAsync(documentId, options);
        
        var isValid = true;
        isValid = documentDatta != null;
        
        if (documentDatta.Size > 10000000)
        {
            return ProcessingResult.Failed("File to large");
        }
        
        await SaveDocumentAsync(documentDatta, options.UserId);
        await _documentRepository.UpdateDocumentStatusAsync(documentId, DocumentStatus.Processed);

        return ProcessingResult.Success(DateTime.Now);
    }
    catch (Exception ex)
    {
        // Rest of the method...

        private async Task<DocumentData> FetchDocumentDataAsync(string documentId, ProcessingOptions options)
        {
            var client = _httpClientFactory.CreateClient("DocumentProcessor");
            if (options.HighPriority)
            {
                client.DefaultRequestHeaders.Add("Priority", "High");
            }

            var response = await client.GetAsync($"{_settings.ApiEndpoint}/documents/{documentId}");
            response.EnsureSuccessStatusCode();
            
            var content = await response.Content.ReadAsStringAsync();
            return JsonConvert.DeserializeObject<DocumentData>(content);
        }

        private async Task SaveDocumentAsync(DocumentData documentData, int userId)
        {
            var processor = GetDocumentProcessor(documentData.Type);
            await processor.ProcessAsync(documentData, userId);
        }

        private IDocumentTypeProcessor GetDocumentProcessor(string documentType)
        {
            return documentType switch
            {
                "invoice" => new InvoiceProcessor(_documentRepository),
                "contract" => new ContractProcessor(_documentRepository),
                _ => new GenericDocumentProcessor(_documentRepository)
            };
        }
    }

    public class ProcessingOptions
    {
        public bool HighPriority { get; set; } = false;
        public int UserId { get; set; }
    }

    public class ProcessingResult
    {
        public bool Success { get; private set; }
        public string ErrorMessage { get; private set; }
        public DateTime? ProcessedAt { get; private set; }

        public static ProcessingResult Success(DateTime processedAt) => 
            new ProcessingResult { Success = true, ProcessedAt = processedAt };
            
        public static ProcessingResult Failed(string errorMessage) => 
            new ProcessingResult { Success = false, ErrorMessage = errorMessage };
    }
    
    // Additional classes would be defined in their own files
}