using HugoBotWebApplication.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace HugoBotWebApplication.ViewModels
{
	public class KarmaLegoIndexViewModel
	{
		public List<Discretization> Discretizations { get; set; }
        public List<KarmaLego> KarmaLegos { get; set; }
        public Dictionary<int,string[]>  Classes{ get; set; }
        public Dataset Dataset { get; set; }
        public readonly string[] RegularMethods = { "EQW", "EQF", "PERSIST", "BINARY", "KMEANS", "SAX" };
        public readonly string[] DistanceMeasureMethods = { "TD4C" };
        public readonly string[] knowledgeBasedMethods = { "EXPERT" };

    }
}