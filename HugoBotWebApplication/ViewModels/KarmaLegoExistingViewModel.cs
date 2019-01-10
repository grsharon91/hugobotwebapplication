using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;

namespace HugoBotWebApplication.ViewModels
{
	public class KarmaLegoExistingViewModel
	{
		public int DiscretizationID { get; set; }
		public double MinimumVerticalSupport { get; set; }
		public int MaximumGap { get; set; }
		public int Epsilon { get; set; }
		public string Visibility { get; set; }
	}
}