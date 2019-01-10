using System.Collections.Generic;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;

namespace HugoBotWebApplication.ViewModels
{
    public class DatasetViewModel
    {
        [Required()]
        public string DatasetName { get; set; }
        [Required()]
        public string Category { get; set; }
        public string Visibility { get; set; }
        public string Type { get; set; }
        [DisplayName("Dataset file")]
        [DataType(DataType.Text)]
        public string Path { get; set; }
        public string VmapPath { get; set; }
		public string DatasetDescription { get; set; }
		public List<string> TemporalPropertyID { get; set; }
		public List<string> TemporalPropertyName { get; set; }
		public List<string> Description { get; set; }
	}
}