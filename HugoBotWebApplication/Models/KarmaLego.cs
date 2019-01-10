using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;

namespace HugoBotWebApplication.Models
{
	public class KarmaLego
	{
		[Required]
		public int KarmaLegoID { get; set; }
		[Required]
		public double MinimumVerticalSupport { get; set; }
		[Required]
		public int MaximumGap { get; set; }
		[Required]
		public double Epsilon { get; set; }
		
        public int Fold { get; set; }

		public string Visibility { get; set; }
		public int DiscretizationID { get; set; }
		public virtual Discretization Discretization { get; set; }
		public string IsReady { get; set; }
        public string DownloadPath { get; set; }
        public string OwnerID { get; set; }

        public virtual ApplicationUser Owner { get; set; }
    }
}