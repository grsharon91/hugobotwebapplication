using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;

namespace HugoBotWebApplication.Models
{
    public class TempDiscretization
    {
        public int TempDiscretizationID { get; set; }
        public string Visibility { get; set; }
        [Required]
        public string Type { get; set; }
        public string Parameters { get; set; }
        public string ParametersIsReady { get; set; }
        public int DatasetID { get; set; }
        public virtual TempDataset Dataset { get; set; }
    }
}