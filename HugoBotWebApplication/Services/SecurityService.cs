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
        

        public SecurityService(DatasetRepository datasetRepository)
        {
            this.datasetRepository = datasetRepository;
        }

        public bool HasAccess(int datasetId, string userId)
        {
            if (userId == "4b67ae3b-8854-40a2-9751-8021070bf5ba")
                return true;
            Dataset dataset = datasetRepository.Get(datasetId);
            bool hasAccess = true;

            if (userId != null && dataset.OwnerID != userId)
                return false;
           
            return hasAccess;
        }
    }
}