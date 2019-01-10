using HugoBotWebApplication.Models;
using HugoBotWebApplication.Models.Formats_Handling;
using System.Collections.Generic;

namespace HugoBotWebApplication.ViewModels
{
    public class MetadataViewModel
    {
		public int TempDatasetId { get; set; }
        public string TempDatasetName { get; set; }
        public Dictionary<int, string[]> Vmap{ get; set; }
        //public Dictionary<string,List<string>> Vmap{ get; set; }
        public string Description { get; set; }
    }
}