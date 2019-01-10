using HugoBotMVC.Services;
using System;
using System.Collections.Generic;
using System.Text;
using System.Xml;

namespace HugoBotMVC
{

    /// <summary>
    /// LegoObjects Class holds a set of claases defining different structures used with the
    /// Lego data.
    /// </summary>
    public static class LegoObjects
    {
        /// <summary>
        /// Represents a Lego pattern, including its properties, relations, statistics
        /// </summary>
        public class LegoPattern
        {
            // List of properties constructing this pattern by order
            public List<LegoProperty> PatternProperties;
            // List of intervals for each property
            public List<TimeSeries.TimeInterval> PatternIntervals;
            // list of relations between each adjacent pair of properties
            public string[] Relations;
            // original instance
            LegoInstance Instance;

            /// <summary>
            /// Copying constructor - given list of pattern's attributes, copying will be made 
            /// and a pattern will be defined
            /// </summary>
            /// <param name="rels">Relations string</param>
            /// <param name="properties">properties list</param>
            /// <param name="instance">instance having this pattern</param>
            public LegoPattern(string rels, List<LegoProperty> properties, LegoInstance instance)
            {

                PatternProperties = new List<LegoProperty>();
                PatternProperties.AddRange(properties);

                PatternIntervals = new List<TimeSeries.TimeInterval>();
                PatternIntervals.AddRange(instance.Intervals);

                Instance = instance;

                Relations = rels.Split(rels[1]);

            } // basic copying constructor

            /// <summary>
            /// get interval coresponding to given property index 
            /// </summary>
            /// <param name="index">given property index</param>
            /// <returns>Time Interval</returns>
            public TimeSeries.TimeInterval GetInterval(int index)
            {
                return PatternIntervals[index];
            } // GetInterval

            /// <summary>
            /// get  a string defining the relation between a  property
            /// and its given consecutive property in the pattern
            /// </summary>
            /// <param name="scndProperty">second  property chronlogically in pair</param>
            /// <returns>Relation string</returns>
            public string GetRelation(int scndProperty)
            {
                return TimeSeries.Intervals.getRelationString(Relations[Methods.N_2(scndProperty + 1) - 1][0]);
            } // GetRelation

            /// <summary>
            /// return entity's ID number
            /// </summary>
            /// <returns></returns>
            public long GetID()
            {
                return Instance.EntityID;
            } // GetID

        } // class LegoPattern

        /// <summary>
        /// represents a list of instances of a given pattern
        /// </summary>
        public class LegoInstancesList
        {
            public int minPoint;
            public int maxPoint;

            //public LegoPattern BasePattern;
            public List<LegoInstance> Instances;

            public List<TimeSeries.TimeInterval> lstAvgIntervals;

            /// <summary>
            /// constructor, needs to know the number of intervals = level
            /// </summary>
            /// <param name="numOfIntervals"></param>
            public LegoInstancesList()
            {
                Instances = new List<LegoInstance>();
                lstAvgIntervals = new List<TimeSeries.TimeInterval>();

                minPoint = int.MaxValue;
                maxPoint = int.MinValue;
            } // basic constructor

            /// <summary>
            /// 
            /// </summary>
            /// <param name="instance"></param>
            public void Add(LegoInstance instance)
            {
                Instances.Add(instance);
                if (instance.Intervals[0].StartTime < minPoint) minPoint = (int)instance.Intervals[0].StartTime;
                if (instance.Intervals[instance.Intervals.Count - 1].EndTime > maxPoint) maxPoint = (int)instance.Intervals[instance.Intervals.Count - 1].EndTime;
                if (lstAvgIntervals.Count == 0)
                {
                    for (int i = 0; i < instance.Intervals.Count; i++)
                        lstAvgIntervals.Add(new TimeSeries.TimeInterval(0, 0));
                } // first time
                for (int i = 0; i < lstAvgIntervals.Count; i++)
                {
                    lstAvgIntervals[i].StartTime += instance.Intervals[i].StartTime;
                    lstAvgIntervals[i].EndTime += instance.Intervals[i].EndTime;
                } // for intervals
            } // add instance

            /// <summary>
            /// returns the length string of a given instance
            /// </summary>
            /// <param name="inst">given instance</param>
            /// <returns>string representing the instance location in time</returns>
            public string getLengthString(LegoInstance inst)
            {
                double mult = (double)Const.INT_INSTANCE_LENGTH_CHARS / (double)(maxPoint - minPoint);
                double bef = ((int)inst.minPoint - minPoint);
                double len = ((int)inst.maxPoint - (int)inst.minPoint);
                double aft = (maxPoint - (int)inst.maxPoint);

                int i;
                string ans = "";

                for (i = 0; i < (int)(mult * bef); i++) ans += " ";
                for (i = 0; i < (int)(mult * len); i++) ans += "-";
                for (i = 0; i < (int)(mult * aft); i++) ans += " ";

                return ans;
            } // getLengthString

            /// <summary>
            /// stop and calculate the Average intervals of current instances list
            /// </summary>
            public void CalculateAvgPatternIntervals()
            {
                int i;
                for (i = 0; i < lstAvgIntervals.Count; i++)
                {
                    lstAvgIntervals[i].StartTime /= Instances.Count;
                    lstAvgIntervals[i].EndTime /= Instances.Count;
                } // for intervals
            } // CalculateAvgPatternIntervals

            public string GetAvgPatternString()
            {
                return Data.getKarmaIntervalsString(lstAvgIntervals);
            }


            public static int[] countInstancesPerUser(LegoInstancesList list, int[] entitiesIDS, int divID)
            {
                int i;
                int[] counters = new int[entitiesIDS.Length];
                for (i = 0; i < counters.Length; i++)
                    counters[i] = 0;

                for (i = 0; i < list.Instances.Count; i++)
                    counters[Methods.Arrays.isMember((int)list.Instances[i].EntityID / divID, entitiesIDS)]++;
                return counters;
            }




        } // class LegoInstancesList

        /// <summary>
        /// represents an instance of a certain pattern, holds relevant data
        /// </summary>
        public class LegoInstance
        {

            public int minPoint;
            public int maxPoint;
            public long EntityID;
            public List<TimeSeries.TimeInterval> Intervals;

            /// <summary>
            /// basic constructor for a lego instance
            /// </summary>
            /// <param name="id">entity's ID</param>
            public LegoInstance(long id)
            {
                EntityID = id;
                Intervals = new List<TimeSeries.TimeInterval>();
                minPoint = int.MaxValue;
                maxPoint = int.MinValue;

            } // basic constructor

            /// <summary>
            /// Add an interval to list of intervals, ordered by properties relations order.
            /// </summary>
            /// <param name="StartTime">start time</param>
            /// <param name="EndTime">end time</param>
            public void AddInterval(long StartTime, long EndTime)
            {

                Intervals.Add(new TimeSeries.TimeInterval(StartTime, EndTime));
                if (StartTime < minPoint) minPoint = (int)StartTime;
                if (EndTime > maxPoint) maxPoint = (int)EndTime;

            } // AddInterval

            /// <summary>
            /// creates a string describing the intervals of this instance
            /// </summary>
            /// <returns></returns>
            public string getIntervalsString()
            {
                int i;
                string ans = "";

                for (i = 0; i < Intervals.Count; i++)
                    ans += Intervals[i].StartTime.ToString() + " - " + Intervals[i].EndTime.ToString() + ", ";
                if (ans != "") ans = ans.Substring(0, ans.Length - 2);
                return ans;

            } // getIntervalsString

        } // class LegoInstance

        /// <summary>
        /// Holds a list of properties (States)
        /// </summary>
        public class LegoPropertiesList
        {
            public List<LegoProperty> PropertiesList;
            public bool blnIsFirstLevel;

            public LegoPropertiesList(bool firstLevel)
            {
                blnIsFirstLevel = firstLevel;
                PropertiesList = new List<LegoProperty>();
            } // basic constructor

            public void Add(LegoProperty property)
            {
                PropertiesList.Add(property);
            } // Add property

            /// <summary>
            /// creates a list of lego properties defined by given list 
            /// of original nodes from XML wekamatrixfile, and assigns it to the current instance of LegoPropertiesList
            /// </summary>
            /// <param name="nodeList"></param>
            public void BuildListFromXmlNodes(XmlNodeList nodeList)
            {
                int i;
                LegoProperty property;

                this.PropertiesList = new List<LegoProperty>();

                for (i = 0; i < nodeList.Count; i++)
                {

                    property = Data.getPropertyFromNode(nodeList[i]);
                    property.propIndex = i;
                    Add(property);

                } // for nodes list

            } // BuildListFromXmlNodes


            /// <summary>
            /// creates a list of lego properties defined by given list 
            /// of original nodes from XML wekamatrixfile, and assigns it to the current instance of LegoPropertiesList
            /// </summary>
            /// <param name="nodeList"></param>
            public void BuildListFromXmlNodes(XmlElement node)
            {
                LegoProperty property;

                this.PropertiesList = new List<LegoProperty>();

                property = Data.getPropertyFromNode(node);
                Add(property);

            } // BuildListFromXmlNodes


        } // class LegoPropertiesList

        /// <summary>
        /// Holds information regarding a certain property
        /// </summary>
        public class LegoProperty
        {
            // State label - i.e property name
            //public string StateLabel;
            public int StateID;
            public long HorizontalSupport;
            public long VerticalSupport;
            public double TIV = 0;
            public string Relations;
            // instances list
            public LegoInstancesList Instances;
            // next level properties
            public LegoPropertiesList NextLevel;

            public bool isLoaded;

            // used for path in results
            public int propIndex;

            // returns the longest path's length in this sub tree (of current property)
            public int depth;

            // For Merged files
            public double meanDuration;
            public long horzSupp_2;
            public long vertSupp_2;
            public double meanDuration_2;

            /// <summary>
            /// Basic constructor 
            /// </summary>
            /// <param name="state">State label</param>
            /// <param name="horzSupp">Horizional support</param>
            /// <param name="vertSupp">Vertical support</param>
            /// <param name="rels">Relations</param>
            public LegoProperty(int stateID, long horzSupp, long vertSupp, string rels)
            {
                StateID = stateID;
                HorizontalSupport = horzSupp;
                VerticalSupport = vertSupp;
                Relations = rels;
                isLoaded = false;
                propIndex = 0;
                depth = 1;
            } // basic constructor
            public LegoProperty(int stateID, long horzSupp, long vertSupp,double meanDuration,long horzSupp_2, long vertSupp_2, double meanDuration_2, string rels)
            {
                StateID = stateID;
                HorizontalSupport = horzSupp;
                VerticalSupport = vertSupp;
                Relations = rels;
                isLoaded = false;
                propIndex = 0;
                depth = 1;

                this.meanDuration = meanDuration;
                this.horzSupp_2 = horzSupp_2;
                this.vertSupp_2 = vertSupp_2;
                this.meanDuration_2 = meanDuration_2;

        } // basic constructor
            /// <summary>
            /// returns a string describing the property
            /// </summary>
            /// <returns>property's string</returns>
            public string ToString(StatesConverter cnv)
            {

                return cnv.getLabel(StateID) + " : " +
                        HorizontalSupport.ToString() + " : " +
                        VerticalSupport.ToString() + " : " +
                        Relations;

            } // ToString

            /// <summary>
            /// runs through the sub tree if this property, updating the depths 
            /// of the subtrees of each level
            /// </summary>
            /// <returns></returns>
            public int updateDepths()
            {
                int temp;
                if (NextLevel == null || NextLevel.PropertiesList.Count == 0)
                {
                    return depth;
                }
                else
                {
                    depth = 0;
                    for (int i = 0; i < NextLevel.PropertiesList.Count; i++)
                    {
                        temp = NextLevel.PropertiesList[i].updateDepths();
                        if (depth < temp)
                            depth = temp + 1;
                    } // for next level properties
                    return depth;
                } // scan sub tree

            } // updateDepths




        } // class LegoProperty


        /// <summary>
        /// general object containing all information related to a specific dataset of lego results
        /// </summary>
        public class LegoResults
        {
            // root element, taken from index wekamatrixfile
            public XmlElement Root;
            // index wekamatrixfile location
            public string strRootLocation;
            // root elements, meaning starting states
            public LegoPropertiesList RootElements;
            // root elements files locations
            public List<string> RootElementsFiles;
            // holds current level of tree (0 for root)
            public int CurrentLevel;
            // holds current path in properties tree
            public List<LegoObjects.LegoProperty> curPropertiesPath;
            // states converter - converts id to label
            public StatesConverter cnvLabels;
            // entities database - including static properties
            public EntitiesData datEntities;

            public IndexFile indexFile;

            public bool blnIsKarmaFiles;


            // HERE HERE HERE
            /// <summary>
            /// LegoResults constructor using karma direct load
            /// </summary>
            /// <param name="filename">Karma wekamatrixfile name</param>
            /// <param name="cnv">States converter object</param>
            /// <param name="datents">Entities data object</param>
            public LegoResults(byte[] indexByteArr, StatesConverter cnv, EntitiesData datents)
            {
                cnvLabels = cnv;

                datEntities = datents;

                CurrentLevel = 0;

                curPropertiesPath = new List<LegoProperty>();

                RootElementsFiles = new List<string>();

                RootElements = new LegoPropertiesList(true);

                blnIsKarmaFiles = true;

                int ind = 0;

                using (KarmaFileReader kr = new KarmaFileReader(indexByteArr))
                {
                    string line = kr.getLine();
                    string[] vals = line.Split(' ');
                    if (vals[0] == "1")
                    {
                        while (line != null)
                        {
                            vals = line.Split(' ');
                            RootElements.Add(Data.parseKarmaPropertyString(vals));
                            RootElements.PropertiesList[ind].isLoaded = false;
                            //RootElements.PropertiesList[ind].Instances = new LegoInstancesList();
                            //RootElements.PropertiesList[ind].NextLevel = new LegoPropertiesList(false);
                            RootElements.PropertiesList[ind].depth = 0;
                            RootElements.PropertiesList[ind].propIndex = ind;
                            ind++;
                            // RootElementsFiles.Add("\\" + kr.getLine());
                            var skipLine = kr.getLine();
                            line = kr.getLine();
                        }
                    } // if it is an index file

                    /* ALON : I think this has no use in our code
                     * else 
                    {
                        int propID = -1;
                        if (int.TryParse(indexfilename.Substring(indexfilename.LastIndexOf('-') + 1, indexfilename.LastIndexOf('.') - indexfilename.LastIndexOf('-') - 1), out propID)) ;
                        // this is a starting property
                        RootElements.Add(new LegoProperty(-1, 0, 0, "UnknownProperty."));
                        RootElements.PropertiesList[0].NextLevel = Data.loadKarmaSubTree(indexfilename);
                        //RootElements.PropertiesList[0].Instances = new LegoInstancesList();
                        RootElements.PropertiesList[0].depth = 0;
                        RootElements.PropertiesList[0].isLoaded = true;
                        //RootElements.PropertiesList[0] = Data.createPropertyData(this, 0);
                        RootElements.PropertiesList[0].updateDepths();
                    } // if it is a specific property file */
                }
            } // Karma wekamatrixfile constructor



            /// <summary>
            /// LegoResults constructor using karma subtrees loading
            /// </summary>
            /// <param name="filename">Karma wekamatrixfile name</param>
            /// <param name="cnv">States converter object</param>
            /// <param name="datents">Entities data object</param>
            public LegoResults(string indexfilename, string basefolder, StatesConverter cnv, EntitiesData datents)
            {
                string path = @"c:\chunk-48.karmac";
                byte[] byteArr = System.IO.File.ReadAllBytes(path);







                cnvLabels = cnv;

                datEntities = datents;

                CurrentLevel = 0;

                curPropertiesPath = new List<LegoProperty>();

                RootElementsFiles = new List<string>();

                RootElements = new LegoPropertiesList(true);

                strRootLocation = basefolder;

                blnIsKarmaFiles = true;

                int ind = 0;

                using (KarmaFileReader kr = new KarmaFileReader(byteArr))
                {
                    string line = kr.getLine();
                    string[] vals = line.Split(' ');
                    if (vals[0] == "1")
                    {
                        while (line != null)
                        {
                            vals = line.Split(' ');
                            RootElements.Add(Data.parseKarmaPropertyString(vals));
                            RootElements.PropertiesList[ind].isLoaded = false;
                            //RootElements.PropertiesList[ind].Instances = new LegoInstancesList();
                            //RootElements.PropertiesList[ind].NextLevel = new LegoPropertiesList(false);
                            RootElements.PropertiesList[ind].depth = 0;
                            RootElements.PropertiesList[ind].propIndex = ind;
                            ind++;
                            RootElementsFiles.Add(basefolder + "\\" + kr.getLine());
                            line = kr.getLine();
                        }

                    } // if it is an index file
                    else
                    {
                        int propID = -1;
                        if (int.TryParse(indexfilename.Substring(indexfilename.LastIndexOf('-') + 1, indexfilename.LastIndexOf('.') - indexfilename.LastIndexOf('-') - 1), out propID)) ;
                        // this is a starting property
                        RootElements.Add(new LegoProperty(-1, 0, 0, "UnknownProperty."));
                        RootElements.PropertiesList[0].NextLevel = Data.loadKarmaSubTree(byteArr, false);
                        //RootElements.PropertiesList[0].Instances = new LegoInstancesList();
                        RootElements.PropertiesList[0].depth = 0;
                        RootElements.PropertiesList[0].isLoaded = true;
                        //RootElements.PropertiesList[0] = Data.createPropertyData(this, 0);
                        RootElements.PropertiesList[0].updateDepths();
                    } // if it is a specific property file
                }

                indexFile = null;

            } // Karma wekamatrixfile constructor



            /// <summary>
            /// LegoResults cnstructor based on XML files. the root is the loaded
            /// index wekamatrixfile's root element
            /// </summary>
            /// <param name="root">Root element of the index wekamatrixfile</param>
            /// <param name="cnv">states converter to use</param>
            /// <param name="datents">participating entities data</param>
            public LegoResults(XmlElement root, StatesConverter cnv, EntitiesData datents)
            {

                int i;

                cnvLabels = cnv;

                datEntities = datents;

                blnIsKarmaFiles = false;

                CurrentLevel = 0;

                curPropertiesPath = new List<LegoProperty>();

                Root = root;

                RootElements = new LegoPropertiesList(true);

                if (Root.Attributes.Count == 4)
                {
                    // this is a starting property
                    RootElements.BuildListFromXmlNodes(root);
                    RootElements.PropertiesList[0].isLoaded = true;
                    RootElements.PropertiesList[0] = Data.createPropertyData(this, 0);
                    RootElements.PropertiesList[0].updateDepths();
                }
                else
                {
                    RootElements.BuildListFromXmlNodes(root.ChildNodes);
                    // save next level information for first level, don't load the whole data shit
                    /*for (i = 0; i < RootElements.PropertiesList.Count; i++)
                    {
                        RootElements.PropertiesList[i].NextLevel = new LegoPropertiesList(false);
                       // RootElements.PropertiesList[i].NextLevel.BuildListFromXmlNodes(root.ChildNodes[i].ChildNodes);
                    }*/
                    // save wekamatrixfile location for each starting state xml
                    RootElementsFiles = new List<string>();
                    for (i = 0; i < root.ChildNodes.Count; i++)
                    {
                        RootElementsFiles.Add(root.ChildNodes[i].Attributes[Const.STR_FILENAME_ATTRIBUTE].Value);
                        //RootElements.PropertiesList[i].NextLevel = Data.getNextLevelFromPropertyFile(RootElementsFiles[RootElementsFiles.Count - 1]);
                    }
                } // normal index
            } // List building constructor







            /// <summary>
            /// get current pattern in tree, use requested instance's intervals.
            /// </summary>
            /// <param name="instanceIndex">Instance to extract (intervals)</param>
            /// <returns>Pattern</returns>
            public LegoObjects.LegoPattern getCurrentPattern(int instanceIndex)
            {
                LegoInstance instance;

                if (curPropertiesPath[CurrentLevel].Instances.Instances.Count == 0)
                    instance = new LegoInstance(-1);
                else
                    instance = curPropertiesPath[CurrentLevel].Instances.Instances[instanceIndex];

                string relations = curPropertiesPath[CurrentLevel].Relations;

                return new LegoPattern(relations, curPropertiesPath, instance);

            } // getCurrentPattern


        } // class LegorResults

    } // class LegoObjects
}
