using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using MyApp.Core.Models.Vouchers;
using MyApp.Core.Services.Interfaces;
using MyApp.Framework;

namespace MyApp.Api.Controllers
{
    [Route("api/vouchers")]
    [ApiController]
    [Authorize]
    public class VoucherController : ControllerBase
    {
        private readonly IVoucherService _voucherService;
        private readonly ILogger<VoucherController> _logger;

        public VoucherController(
            IVoucherService voucherService,
            ILogger<VoucherController> logger)
        {
            _voucherService = voucherService ?? throw new ArgumentNullException(nameof(voucherService));
            _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        }

        [HttpGet]
        [ProducesResponseType(typeof(IEnumerable<VoucherDto>), StatusCodes.Status200OK)]
        public async Task<IActionResult> GetVouchersAsync([FromQuery] VoucherSearchCriteria criteria)
        {
            _logger.LogInformation($"User {User.Identity.Name} retrieving vouchers");
            
            var result = await _voucherService.GetVouchersAsync(criteria);
            return Ok(result);
        }

        [HttpGet("{id}")]
        [ProducesResponseType(typeof(VoucherDto), StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<IActionResult> GetVoucherByIdAsync([FromRoute] int id)
        {
            var voucher = await _voucherService.GetVoucherByIdAsync(id);
            
            if (voucher == null)
            {
                return NotFound();
            }
            
            return Ok(voucher);
        }

        [HttpPost]
        [ProducesResponseType(typeof(VoucherDto), StatusCodes.Status201Created)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        public async Task<IActionResult> CreateVoucherAsync([FromBody] CreateVoucherDto voucherDto)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            try
            {
                var result = await _voucherService.CreateVoucherAsync(voucherDto);
                return CreatedAtAction(nameof(GetVoucherByIdAsync), new { id = result.Id }, result);
            }
            catch (ValidationException ex)
            {
                return BadRequest(ex.Message);
            }
        }

        [HttpPut("{id}")]
        [ProducesResponseType(StatusCodes.Status204NoContent)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<IActionResult> UpdateVoucherAsync(int id, [FromBody] UpdateVoucherDto voucherDto)
        {
            if (id != voucherDto.Id)
            {
                return BadRequest("ID in route must match ID in body");
            }

            try
            {
                var exists = await _voucherService.VoucherExistsAsync(id);
                if (!exists)
                {
                    return NotFound();
                }

                await _voucherService.UpdateVoucherAsync(voucherDto);
                return NoContent();
            }
            catch (ValidationException ex)
            {
                return BadRequest(ex.Message);
            }
        }
    }
}