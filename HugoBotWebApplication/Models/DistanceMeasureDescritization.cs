using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;

namespace HugoBotWebApplication.Models
{
    public class DistanceMeasureDescritization : Discretization
    {
        //public int DiscretizationID { get; set; }
        //public string Visibility { get; set; }
        //[Required]
        //public string Type { get; set; }
        //public string ParametersIsReady { get; set; }
        //public int DatasetID { get; set; }
        //public virtual Dataset Dataset { get; set; }
        //public virtual List<KarmaLego> KarmaLegos { get; set; }
        //public string OwnerID { get; set; }
        //public virtual ApplicationUser Owner { get; set; }
        //public string DownloadPath { get; set; }
        //public string FullName { get; set; }
        //public int BinsNumber { get; set; }
        //public int WindowSize { get; set; }
        //public int MaxGap { get; set; }
        public string DistanceMeasure { get; set; }
    }
}