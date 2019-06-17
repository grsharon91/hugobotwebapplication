using System.Collections.Generic;
using HugoBotWebApplication.Models;

namespace HugoBotWebApplication.ViewModels
{
    public class DatasetIndexViewModel
    {
        public List<Dataset> Datasets { get; set; }
        public List<string> DatasetsRecords { get; set; }
        public List<string> DiscretizationsRecords { get; set; }
		public List<string> KarmaLegoRecords { get; set; }
        public List<ViewPermissions> ViewPermissionsRecords { get; set; }
		public string abc { get; set; }


    }
}