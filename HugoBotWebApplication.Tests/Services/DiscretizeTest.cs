using System;
using HugoBotWebApplication.Services;
using Microsoft.VisualStudio.TestTools.UnitTesting;


namespace HugoBotWebApplication.Tests.Services
{
    [TestClass]
    public class DiscretizeTest
    {
        DiscretizationService discretizationService = new DiscretizationService();

        [TestMethod]
        public void TestDiscretize()
        {
            //var pathStub = new stubPath();
            //pathStub.Combine = (value) => "a";
           // var pathStub = Mock.Create();

            string[] methodsList = { "EQW", "EQf" };
            string ans = discretizationService.Discretize(methodsList, "~/dataset.csv" );

        }
    }
}
