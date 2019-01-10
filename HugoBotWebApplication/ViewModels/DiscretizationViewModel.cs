using System.Collections.Generic;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using System.Web;

namespace HugoBotWebApplication.ViewModels
{
    public class DiscretizationViewModel

    {
        public DiscretizationViewModel()
        {
        }

        [Required()]
        public string DatasetName { get; set; }
        [Required()]
        public string Category { get; set; }
        public string Visibility { get; set; }
        public int Rating { get; set; }
        public string Type { get; set; }
        public string Parameters { get; set; }
        [DisplayName("Dataset file")]
        [DataType(DataType.Text)]
        public string Path { get; set; }
        //[Required(ErrorMessage = "Please choose at least one abstraction method")]
        [DataType(DataType.Text)]
        public string AbstractionMethodsFullNames { get; set; }
        [DataType(DataType.Text)]
        public string AbstractionFullEncoding { get; set; }
        [Required(ErrorMessage = "Please fill in bins number")]
        [Range(1, int.MaxValue)]
        public int BinsNumber { get; set; }

       
        public bool AbstractedTimeSeries { get; set; }
        public int? MaxGap { get; set; }
        public string VmapPath { get; set; }
        [Required]
        public List<string> abstraction_method { get; set; }
        public List<string> td4c_param { get; set; }
        public HttpPostedFileBase expert_param { get; set; }
		public int? sax_param { get; set; }
		public string Description { get; set; }
        public string expert_Path { get; set; }
		//public bool eqw { get; set; }
		//public bool eqf { get; set; }
		//public bool persist { get; set; }
		//public bool binary { get; set; }
		//public bool td4c { get; set; }
		//public bool td4c_e { get; set; }
		//public bool td4c_c { get; set; }
		//public bool td4c_k { get; set; }

	}
}