using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;

namespace HugoBotWebApplication.Models
{
    public class TempDataset
    {
        public int TempDatasetID { get; set; }
        [Required()]
        public string DatasetName { get; set; }
        [Required()]
        public string Category { get; set; }
        public string Visibility { get; set; }
        public int Rating { get; set; }
        [Required]
        public string Type { get; set; }
        public string Parameters { get; set; }
        public string ParametersIsReady { get; set; }
        [DataType(DataType.Text)]
        public string Path { get; set; }
      
        [DataType(DataType.Text)]
        public string VmapPath { get; set; }
        public string Description { get; set; }
        //[ForeignKey("ApplicationUser")]
        //public string ApplicationUserID { get; set; }

      
        public virtual List<TempDiscretization> Discretizations { get; set; }
        public TempDataset()
        {

        }
        public TempDataset(Dataset dataset)
        {
            TempDatasetID = dataset.DatasetID;
            DatasetName = dataset.DatasetName;
            Category = dataset.Category;
            Visibility = dataset.Visibility;
            Rating = dataset.Rating;
            Type = dataset.Type;
            Parameters = dataset.Parameters;
            ParametersIsReady = dataset.ParametersIsReady;
            Path = dataset.Path;
            VmapPath = dataset.VmapPath;
            Description = dataset.Description;
        }
    }
}