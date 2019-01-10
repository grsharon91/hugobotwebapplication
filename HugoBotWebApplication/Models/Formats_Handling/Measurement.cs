using FileHelpers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace HugoBotWebApplication.Models.Formats_Handling
{
    [DelimitedRecord(",")]
    [IgnoreFirst(1)]
    public class Measurement
    {
        [FieldOrder(1), FieldTitle("EntityID")]
        public int EntityID;
        [FieldOrder(2), FieldTitle("TemporalPropertyID")]
        public int TemporalPropertyID;
        [FieldOrder(3), FieldTitle("TimeStamp")]
        public int TimeStamp;
        [FieldOrder(4), FieldTitle("TemporalPropertyValue")]
        public double TemporalPropertyValue;
    }
}