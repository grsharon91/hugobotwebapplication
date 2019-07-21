using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Web;

namespace HugoBotWebApplication.Models
{
    public class Dataset
    {
        public int DatasetID { get; set; }
        [Required()]
        public string DatasetName{ get; set; }
        [Required()]
        public string Category { get; set; }
        public string Visibility { get; set; }
        public int Rating { get; set; }
        [Required]
        public string Type { get; set; }
        public string Parameters { get; set; }
        public string ParametersIsReady { get; set; }
       // [Required()]
       // [DisplayName("Dataset file")]
       // [DataType(DataType.Text)]
       [NotMapped]
        public string Path { get; set; }
       // [Required()]
       // [DisplayName("Vmap file")]
       // [DataType(DataType.Text)]
       [NotMapped]
        public string VmapPath { get; set; }
		public string Description { get; set; }
		public string OwnerID { get; set; }

        public virtual ApplicationUser Owner { get; set; }
        public virtual List<Discretization> Discretizations { get; set; }


        public int NumberOfDownloads { get; set; }
        public int NumberOfViews { get; set; }
        public double Size { get; set; }
        public DateTime DateUploaded{ get; set; }
        public string EntitiesPath { get; set; }
        public int hasClass { get; set; }

        public byte [] metaData { get; set; }
        public byte [] DatasetFile { get; set; }

    }
}