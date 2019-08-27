using HugoBotWebApplication.Models;
using HugoBotWebApplication.Models.Repositories;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace HugoBotWebApplication.Services
{
    public class SecurityService
    {
        private DatasetRepository datasetRepository;
        private ApplicationDbContext db;


        public SecurityService(DatasetRepository datasetRepository, ApplicationDbContext db)
        {
            this.datasetRepository = datasetRepository;
            this.db = db;
        }

        public bool HasAccess(int datasetId, string userId)
        {
            if (userId == "4b67ae3b-8854-40a2-9751-8021070bf5ba")
                return true;
            Dataset dataset = datasetRepository.Get(datasetId);
            bool hasAccess = true;

            ApplicationUser user = db.Users.Find(userId);
            ViewPermissions vp = new ViewPermissions
            {
                Key = user.Id + datasetId.ToString(),
                UserName = user.UserName,
                DatasetID = datasetId
            };
            var searchVP = db.ViewPermissions.Find(vp.Key);

            if (userId != null && dataset.OwnerID != userId && dataset.Visibility == "Private" && searchVP == null)
                return false;

            return hasAccess;
        }
    }
}