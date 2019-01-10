using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace HugoBotWebApplication.Utils
{
    public static class Settings
    {
        private static readonly Dictionary<string, string> methodEncodingToMethodName = new Dictionary<string, string>()
                {
                    {"EQW", "Equal Width" },
                    {"EQF", "Equal Frequency" },
                    {"PERSIST", "Persist" },
                    {"EXPERT", "Expert" },
                    {"KMEANS", "Kmeans" },
                    {"BINARY", "Binary" },
                    {"TD4C", "TD4C" },
                    {"SAX", "SAX" },
                    {"KARMALEGO", "KarmaLego"}
                };

        private static readonly List<string> distanceMeasureMethods = new List<string> {"TD4C"};

        public static Dictionary<string, string> MethodEncodingToMethodName => methodEncodingToMethodName;

        public static List<string> DistanceMeasureMethods => distanceMeasureMethods;
    }
}