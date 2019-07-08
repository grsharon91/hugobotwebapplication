using HugoBotWebApplication.Models;
using HugoBotWebApplication.Models.Formats_Handling;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace HugoBotWebApplication.ViewModels
{
	public class DatasetDetailsViewModel
	{
		public int DatasetID { get; set; }
		public string DatasetName { get; set; }
		public string Category { get; set; }
		public string Visibility { get; set; }
		public int Rating { get; set; }
		public string Type { get; set; }
		public string Parameters { get; set; }
		public string ParametersIsReady { get; set; }
        public Dataset Dataset { get; set; }
        public string Path { get; set; }

		public string VmapPath { get; set; }
		public string Description { get; set; }

		public string OwnerID { get; set; }

		public virtual ApplicationUser Owner { get; set; }
		public virtual List<Discretization> Discretizations { get; set; }
		public VariableMetadata[] Metadata {get; set;}
		public int NumberOfEntities { get; set; }
		public int NumberOfProperties { get; set; }
        public string DatasetSource { get; set; }

    }
}