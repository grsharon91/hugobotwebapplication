using System;
using System.Collections.Generic;
using HugoBotMVC.Services;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace HugoBotWebApplication.Tests.Services
{
    [TestClass]
    public class AttributeTest
    {

        private HugoBotMVC.Services.Attribute attribute = new HugoBotMVC.Services.Attribute("test_attribute");

        [TestMethod]
        public void TestGetDataAsDictionary()
        {
            List<int> emptyList = null;
            Dictionary<string, List<int>> data = (Dictionary<string, List<int>>)attribute.getDataAsDictionary();
            data.TryGetValue("data", out emptyList);
            Assert.IsNotNull(emptyList);
        }

        [TestMethod]
        public void TestGetDataAsDictionaryWithData()
        {
            Dictionary<string, int> oldValueCount = attribute.valuesCount;
            Dictionary<string, int> valueCount = new Dictionary<string, int>();
            valueCount.Add("test1", 1);
            valueCount.Add("test2", 2);
            attribute.valuesCount = valueCount;
            List<int> list = null;
            Dictionary<string, List<int>> data = (Dictionary<string, List<int>>)attribute.getDataAsDictionary();
            data.TryGetValue("data", out list);
            Assert.IsNotNull(list);
            Assert.AreEqual(list.IndexOf(1), 0);
            Assert.AreEqual(list.IndexOf(2), 1);
            attribute.valuesCount = oldValueCount;
            
        }

        [TestMethod]
        public void TestGetLabels()
        {
            Dictionary<string, int> oldValueCount = attribute.valuesCount;
            Dictionary<string, int> valueCount = new Dictionary<string, int>();
            valueCount.Add("test1", 1);
            valueCount.Add("test2", 2);
            attribute.valuesCount = valueCount;
            List<string> list = attribute.getLabels();
            Assert.IsNotNull(list);
            Assert.IsTrue(list.Contains("test1"));
            Assert.IsTrue(list.Contains("test2"));
            Assert.IsFalse(list.Contains("test3"));
            attribute.valuesCount = oldValueCount;

        }
    }
}
