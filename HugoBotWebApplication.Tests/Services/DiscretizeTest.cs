using System;
using System.Collections.Generic;
using HugoBotWebApplication.Models;
using HugoBotWebApplication.Services;
using Microsoft.VisualStudio.TestTools.UnitTesting;


namespace HugoBotWebApplication.Tests.Services
{
    [TestClass]
    public class DiscretizeTest
    {
        DiscretizationService discretizationService = new DiscretizationService();

        [TestMethod]
        public void TestGetPath()
        {

            List<Discretization> discretizations = new List<Discretization>();
            Discretization discretization = new Discretization();
            discretization.DownloadPath = "this is download path";
            discretizations.Add(discretization);
            string downloadPaths = discretizationService.GetDownloadPath(discretizations);
            Assert.IsNotNull(downloadPaths);
            Assert.AreEqual(downloadPaths, "this is download path");
        }

        [TestMethod]
        public void TestGetFullMethodName()
        {
            string shortName = "EQF";
            string fullName = discretizationService.getFullMethodName(shortName, "");
            Assert.AreEqual(fullName, "equal-frequency");
            shortName = "TD4C";
            string distanceMeasure = "Cosine";
            fullName = discretizationService.getFullMethodName(shortName, distanceMeasure);
            Assert.AreEqual(fullName, "td4c-cosine");
        }
    }
}
