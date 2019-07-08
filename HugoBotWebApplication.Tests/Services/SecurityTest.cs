using System;
using HugoBotWebApplication.Services;
using HugoBotWebApplication.Models;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using HugoBotWebApplication.Models.Repositories;

namespace HugoBotWebApplication.Tests.Services
{
    [TestClass]
    public class SecurityTest
    {
        static ApplicationDbContext db = new ApplicationDbContext();
        static DatasetRepository datasetRepository = new DatasetRepository(db);
        SecurityService securitySerivice = new SecurityService(datasetRepository, db);


        [TestMethod]
        public void TestHasAccess()
        {
            bool ans;
            string userid;
            int datasetID;

        }
    }
}
