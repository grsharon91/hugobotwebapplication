using FileHelpers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace HugoBotWebApplication.Models.Formats_Handling
{
    [DelimitedRecord(",")]
    [IgnoreFirst(1)]
    public class VariableMetadata
    {
        public int TemporalPropertyID { get; set; }
        public string TemporalPropertyName { get; set; }
		public string Description { get; set; }
    }
}