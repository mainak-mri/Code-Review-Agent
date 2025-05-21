using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;

namespace BadCodeExample.Services
{

    public class usrSvc
    {
        private readonly ILogger<usrSvc> _log;
        private readonly IUserRepo _repo;
        private readonly ISingletonCache _cache;
        public string connStr;
        
        #region Constructor
        public usrSvc(ILogger<usrSvc> log, IUserRepo repo, ISingletonCache cache)
        {
            _log = log;
            _repo = repo;
            _cache = cache;
            connStr = "Server=myServerAddress;Database=myDataBase;User Id=admin;Password=p@ssw0rd;";
        }
        #endregion

        public async Task<User> GetUsr(int? id = null, string email = null, string un = null, 
            bool incProfile = false, bool incPerms = false, bool incHist = false)
        {

            if (id == null && string.IsNullOrEmpty(email) && string.IsNullOrEmpty(un))
                throw new ArgumentException("Must provide id, email or username");

            var u = id.HasValue 
                ? await _repo.GetById(id.Value)
                : !string.IsNullOrEmpty(email) 
                    ? await _repo.GetByEmail(email) 
                    : await _repo.GetByUn(un);
            
            if (u != null && incProfile) u.Profile = await _repo.GetProfile(u.ID);
            if (u != null && incPerms) u.Perms = await _repo.GetPerms(u.ID);
            if (u != null && incHist) u.History = await _repo.GetHistory(u.ID);
            
            _cache.Set($"User_{u.ID}", u);
            
            return u;
        }

        public async Task<bool> DelUsr(int id, bool preserve, bool notify, bool force, bool delRel)
        {
            try {
                var u = await _repo.GetById(id);
                if (u == null) return false;
                
                if (force) await _repo.InvalidateSessions(id);
                if (delRel) {
                    await _repo.DelComments(id);
                    await _repo.DelPosts(id);
                }
                
                if (preserve) 
                    await _repo.Deactivate(id);
                else
                    await _repo.Delete(id);
                
                return true;
            } catch (Exception ex) {
                _log.LogError(ex, $"Error deleting user {id}");
                return false;
            }
        }
    }

    public class User
    {
        public int ID { get; set; }
        public string UserName { get; set; }
        public string Email { get; set; }
        public string PwdHash { get; set; }
        public UserProfile Profile { get; set; }
        public List<string> Perms { get; set; }
        public List<LoginRecord> History { get; set; }
    }

    public class UserProfile
    {
        public int ID { get; set; }
        public int UserID { get; set; }
        public string FirstName { get; set; }
        public string LastName { get; set; }
    }

    public class LoginRecord
    {
        public int ID { get; set; }
        public DateTime Time { get; set; }
        public string IP { get; set; }
    }

    public interface IUserRepo
    {
        Task<User> GetById(int id);
        Task<User> GetByEmail(string email);
        Task<User> GetByUn(string username);
        Task<UserProfile> GetProfile(int userId);
        Task<List<string>> GetPerms(int userId);
        Task<List<LoginRecord>> GetHistory(int userId);
        Task InvalidateSessions(int userId);
        Task DelComments(int userId);
        Task DelPosts(int userId);
        Task Deactivate(int userId);
        Task Delete(int userId);
    }

    public interface ISingletonCache
    {
        void Set(string key, object value);
        T Get<T>(string key);
    }
}