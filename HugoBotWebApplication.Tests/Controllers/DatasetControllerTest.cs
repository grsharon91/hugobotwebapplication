using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Web.Mvc;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using HugoBotWebApplication;
using HugoBotWebApplication.Controllers;

namespace HugoBotWebApplication.Tests.Controllers
{
    [TestClass]
    public class DatasetControllerTest
    {
        [TestMethod]
        public void Index()
        {

            //Arrange
            DatasetsController controller = new DatasetsController();

            //Act
            ViewResult result = controller.Index() as ViewResult;

            //Assert
            Assert.IsNotNull(result);
        }


    }
}
