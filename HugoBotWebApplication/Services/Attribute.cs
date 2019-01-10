using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace HugoBotMVC.Services
{
    public class Attribute
    {
        public string name;
        public Dictionary<string, int> valuesCount = new Dictionary<string, int>();

        public Attribute(string _name)
        {
            this.name = _name;
        }

        public object getDataAsDictionary()
        {

            Dictionary<string, List<int>> data = new Dictionary<string, List<int>>();

            data.Add("data", new List<int>());

            foreach (KeyValuePair<string, int> entry in valuesCount)
            {
                data["data"].Add(entry.Value);
            }

            return data;
        }

        public List<string> getLabels()
        {

            List<string> labels = new List<string>();

            foreach (KeyValuePair<string, int> entry in valuesCount)
            {
                labels.Add(entry.Key);
            }

            return labels;
        }
    
    }
}