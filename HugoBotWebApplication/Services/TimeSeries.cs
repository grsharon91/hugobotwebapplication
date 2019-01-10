namespace HugoBotMVC.Services
{
    public static class TimeSeries
    {

        public static class Intervals
        {
            /// <summary>
            /// get a string describing the relation (extends the single char)
            /// </summary>
            /// <param name="rel">given relation char</param>
            /// <returns>relation string</returns>
            public static string getRelationString(char rel)
            {
                switch (rel)
                {
                    case 's': { return "Starts"; }
                    case 'S': { return "Started By"; }
                    case 'c': { return "Contains"; }
                    case 'm': { return "Meets"; }
                    case 'b': { return "Before"; }
                    case 'o': { return "Overlaps"; }
                    case 'e': { return "Equals"; }
                    case 'F': { return "Finishes By"; }
                    default: { return "No Relation"; }
                } // switch

            } // getRelationString

        } // class Intervals

        /// <summary>
        /// Handles a time interval (the time between 2 time points}
        /// </summary>
        public class TimeInterval
        {
            public long StartTime;
            public long EndTime;

            /// <summary>
            /// basic constructor, getting start and end time
            /// </summary>
            /// <param name="startt">start time</param>
            /// <param name="endt">end time</param>
            /// 

            public TimeInterval() { }

            public TimeInterval(long startt, long endt)
            {
                StartTime = startt;
                EndTime = endt;
            } // basic constructor

            /// <summary>
            /// length of interval
            /// </summary>
            /// <returns></returns>
            public long length()
            {
                return EndTime - StartTime;
            } // Length

        } // class TimeInterval

    } // class TimeSeries
}
