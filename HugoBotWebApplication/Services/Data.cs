using System;
using System.Collections.Generic;
using System.Drawing;
using System.Text;
using System.Xml;
using System.IO;
using System.Data;
using HugoBotMVC.Services;

namespace HugoBotMVC
{

    /// <summary>
    /// used to load and save CSV files using DataTables
    /// </summary>
    public static class CSVExporter
    {

        /// <summary>
        /// loads a CSV wekamatrixfile to a dataset, where first column is index
        /// </summary>
        /// <param name="fileName">CSV wekamatrixfile name</param>
        /// <returns>dataset including the data from the wekamatrixfile</returns>
        public static DataSet loadCSVtoDataSetIndexed(byte[] byteArr)
        {
            object[] rowvals;
            string[] values;
            string line;
            int i;

            DataSet ds = new DataSet();
            ds.Tables.Add(new DataTable());


            using (StreamReader sr = new StreamReader(new MemoryStream(byteArr), Encoding.Default))
            {
                values = sr.ReadLine().Split(',');
                ds.Tables[0].Columns.Add(values[0], Type.GetType("System.Int32"));
                for (i = 1; i < values.Length; i++)
                    ds.Tables[0].Columns.Add(values[i]);

                rowvals = new object[values.Length];

                while ((line = sr.ReadLine()) != null)
                {
                    values = line.Split(',');

                    rowvals[0] = int.Parse(values[0]);
                    for (i = 1; i < rowvals.Length; i++)
                        rowvals[i] = values[i];
                    ds.Tables[0].Rows.Add(rowvals);
                } // add lines

            } // using

            return ds;

        } // loadCSVtoDataSetIndexed


        /// <summary>
        /// loads a CSV wekamatrixfile to a dataset
        /// </summary>
        /// <param name="fileName">CSV wekamatrixfile name</param>
        /// <returns>dataset including the data from the wekamatrixfile</returns>
        public static DataSet loadCSVtoDataSet(byte[] byteArr)
        {
            string[] values;
            string line;

            DataSet ds = new DataSet();
            ds.Tables.Add(new DataTable());

            using (StreamReader sr = new StreamReader(new MemoryStream(byteArr), Encoding.Default))
            {
                values = sr.ReadLine().Split(',');
                for (int i = 0; i < values.Length; i++)
                    ds.Tables[0].Columns.Add(values[i]);

                while ((line = sr.ReadLine()) != null)
                {
                    values = line.Split(',');
                    ds.Tables[0].Rows.Add(values);
                }
            }
            return ds;

        } // loadCSVtoDataSet

        /// <summary>
        /// saves the given DataTable using CSV format to the given wekamatrixfile path.
        /// </summary>
        /// <param name="fileName">wekamatrixfile path</param>
        /// <param name="table">DataTable object</param>
        public static void saveDataTableToCSV(string fileName, DataTable table)
        {
            int i, j;
            string strLine = "";

            using (StreamWriter sw = new StreamWriter(fileName))
            {
                strLine = table.Columns[0].ColumnName;
                for (i = 1; i < table.Columns.Count; i++)
                    strLine += "," + table.Columns[i].ColumnName;
                sw.WriteLine(strLine);
                strLine = "";
                for (i = 0; i < table.Rows.Count; i++)
                {
                    strLine = table.Rows[i][table.Columns[0].ColumnName].ToString();
                    for (j = 1; j < table.Columns.Count; j++)
                        strLine += "," + table.Rows[i][table.Columns[j].ColumnName].ToString();
                    sw.WriteLine(strLine);
                } // for rows
            } // using
        } // saveDataTableToCSV

        public static string getDataRowCSVFormatFix(DataRow row, int fix)
        {
            string ans;
            ans = fix.ToString();
            for (int i = 1; i < row.ItemArray.Length; i++)
                ans += "," + row.ItemArray[i].ToString();

            return ans;
        } // getDataRowCSVFormatFix

    } // class CVSExporter

    /// <summary>
    /// Holds Files names of current dataset
    /// </summary>
    public class FilesNames
    {
        public string fileIndex;
        public string fileCSV;
        public string fileStatic;

        public FilesNames(string fileind, string filecsv, string filestat)
        {
            fileStatic = filestat;
            fileIndex = fileind;
            fileCSV = filecsv;
        } // basic constructor
    } // class FileNames

    public class EntitiesData
    {
        DataTable data;

        /// <summary>
        /// class constructor : get data from wekamatrixfile and store in dataset
        /// </summary>
        /// <param name="csvFilename">data wekamatrixfile name</param>
        public EntitiesData(byte[] byteArr)
        {
            data = CSVExporter.loadCSVtoDataSetIndexed(byteArr).Tables[0];
        } // basic constructor


        /// <summary>
        /// get entity ID by the instance's index
        /// </summary>
        /// <param name="index">index of entity in list of entities</param>
        /// <returns></returns>
        public int getEntityID(int index)
        {
            return (int)data.Rows[index][0];
        }

        /// <summary>
        /// returns number of entities in data
        /// </summary>
        /// <returns></returns>
        public int getEntitiesCount()
        {
            return data.Rows.Count;
        }

        /// <summary>
        /// returns a list of available properties names
        /// </summary>
        /// <returns></returns>
        public List<string> getPropertiesList()
        {
            int i;
            List<string> list = new List<string>();
            for (i = 0; i < data.Columns.Count; i++)
                list.Add(data.Columns[i].Caption);
            return list;

        } // getPropertiesList

        /// <summary>
        /// runs a query over the entities data
        /// </summary>
        /// <param name="ID">entity's id </param>
        /// <param name="property">property's name</param>
        /// <returns>property value</returns>
        public string Query(int ID, string property)
        {
            string colEntityID = data.Columns[0].ColumnName;
            DataRow[] row = data.Select(colEntityID + "=" + ID.ToString(), colEntityID);
            return row[0][property].ToString();
        } // Query


        /// <summary>
        /// Used to load data for the pie graph
        /// </summary>
        /// <param name="list">lst of instances</param>
        /// <param name="property">Create table of this property</param>
        /// <returns>a 2 columns list of the possible values and their count (in number of entities)</returns>
        public object[][] ResolveStatisticData(LegoObjects.LegoInstancesList list, string property)
        {

            string str;
            List<string> vals = new List<string>();
            List<int> counts = new List<int>();

            int i, j;

            for (i = 0; i < list.Instances.Count; i++)
            {
                str = Query((int)list.Instances[i].EntityID, property);
                if (vals.Contains(str))
                    counts[vals.IndexOf(str)]++;
                else
                {
                    vals.Add(str);
                    counts.Add(1);
                } // first encounter

            }//for instances

            object[][] res = new object[2][];
            res[0] = vals.ToArray();
            res[1] = new object[counts.Count];
            for (j = 0; j < counts.Count; j++)
                res[1][j] = counts[j];
            return res;

        } // ResolveStatisticData

        /// <summary>
        /// find entity and return its index in the list
        /// </summary>
        /// <param name="ID">entity id to find</param>
        /// <returns>row number in the datatable of entities</returns>
        public int getEntityIndex(int ID)
        {
            int ans = -1, i = -1;
            while (ans == -1 && i < data.Rows.Count)
                if (data.Rows[++i][data.Columns[0].ColumnName].ToString() == ID.ToString())
                    ans = i;
            return ans;
        } // GetEntityIndex

        public DataTable getData()
        {
            return this.data;
        }

    } // class EntitiesData

    public class StatesConverter
    {

        private DataSet dsStateInfo;
        private Dictionary<int, string> dicStates;
        private Dictionary<int, Color> dicColors;

        public StatesConverter(byte[] byteArr)
        {
            int i;

            dsStateInfo = CSVExporter.loadCSVtoDataSet(byteArr);

            dicStates = new Dictionary<int, string>();

            dicColors = new Dictionary<int, Color>();

            //arrStatesColors = new Color[dsStateInfo.Tables[0].Rows.Count];

            for (i = 0; i < dsStateInfo.Tables[0].Rows.Count; i++)
            {
                dicColors.Add(int.Parse(dsStateInfo.Tables[0].Rows[i][Const.STR_STATE_ID].ToString()), Color.FromArgb(Program.randNumber.Next(0, 255), Program.randNumber.Next(0, 255), Program.randNumber.Next(0, 255)));
                dicStates.Add(int.Parse(dsStateInfo.Tables[0].Rows[i][Const.STR_STATE_ID].ToString()), dsStateInfo.Tables[0].Rows[i][Const.STR_TEMPORAL_PROPERTY_NAME].ToString() + "." + dsStateInfo.Tables[0].Rows[i][Const.STR_BIN_LABEL].ToString());
            }
        } // basic constructor

        public Dictionary<int, string> getDicStates()
        {
            return this.dicStates;
        }


        /// <summary>
        /// returns state name by its id : propertyname.binlabel
        /// </summary>
        /// <param name="id">given id of state</param>
        /// <returns>state's label</returns>
        public string getLabel(int id)
        {
            string name;
            if (dicStates.TryGetValue(id, out name))
                return name;
            else
                return "not_found";

        } // getStateName

        /// <summary>
        /// returns the color chosen for the given state
        /// </summary>
        /// <param name="id"></param>
        /// <returns></returns>
        public Color getColor(int id)
        {
            Color col;
            if (dicColors.TryGetValue(id, out col))
                return col;
            else
                return Color.FromArgb(Program.randNumber.Next(0, 255), Program.randNumber.Next(0, 255), Program.randNumber.Next(0, 255));
        } // getColor

    } // StateConverter

    public class Data
    {

        /// <summary>
        /// repairs a wekamatrixfile name in order to be written in an xml
        /// </summary>
        /// <param name="filename">string to be repaired</param>
        /// <returns>repaired string</returns>
        public static string repairFilename(string filename)
        {

            if (filename.IndexOf('[') != -1) filename = filename.Replace("[", "-");
            if (filename.IndexOf(']') != -1) filename = filename.Replace("]", "-");

            return filename;
        }// repairFileName


        #region XMLStructures

        /// <summary>
        /// create property from a given node
        /// </summary>
        /// <param name="node">given node</param>
        /// <returns>new property</returns>
        public static LegoObjects.LegoProperty getPropertyFromNode(XmlNode node)
        {
            string[] vals;
            string prms = node.Attributes["prms"].Value.ToString();
            vals = prms.Split('-');
            prms = vals[vals.Length - 2];
            long vSupp = long.Parse(node.Attributes["vsup"].Value.ToString());
            long hSupp = (long)double.Parse(node.Attributes["mhsup"].Value.ToString());
            string rels = node.Attributes["rels"].Value.ToString();
            if (rels[0] == '\0') rels = "";

            return new LegoObjects.LegoProperty(int.Parse(prms), hSupp, vSupp, rels);

        } // getPropertyFromNode

        /// <summary>
        /// returns the next level list from a given wekamatrixfile, used to show a preview of the next level
        /// </summary>
        /// <param name="fileName">property's wekamatrixfile name</param>
        /// <param name="toLevel">load till this level</param>
        /// <returns>loaded next level properties list</returns>
        public static LegoObjects.LegoPropertiesList getNextLevelFromPropertyFile(string fileName, int toLevel)
        {

            XmlDocument xmdDoc = new XmlDocument();
            xmdDoc.Load(fileName);
            return getNextPropertiesList(xmdDoc.DocumentElement, toLevel);

        } // getNextLevelFromPropertyFile


        /// <summary>
        /// Create next level list of properties using sub TIRP tags of a given element
        /// </summary>
        /// <param name="property">element to extract list from</param>
        /// <returns>Properties list object</returns>
        public static LegoObjects.LegoPropertiesList getNextPropertiesList(XmlNode property, int toLevel)
        {

            if (toLevel == 0) return new LegoObjects.LegoPropertiesList(false);
            int i;
            LegoObjects.LegoPropertiesList properties = new LegoObjects.LegoPropertiesList(false);
            LegoObjects.LegoProperty newProperty;
            //string[] vals;
            //string[] vals2;
            //List<TimeSeries.TimeInterval> intervals;

            XmlNodeList propNodeList = property.SelectNodes(Const.STR_TIRP_TAG);

            for (i = 0; i < propNodeList.Count; i++)
            {
                newProperty = getPropertyFromNode(propNodeList[i]);
                newProperty.NextLevel = getNextPropertiesList(propNodeList[i], --toLevel);
                properties.Add(newProperty);

            } // for nodes

            return properties;

        } // getInstancesList


        /// <summary>
        /// create instances list by a given XmlElement property (level 2 and up)
        /// </summary>
        /// <param name="property">element to extract list from</param>
        /// <returns>InstancesList object</returns>
        public static LegoObjects.LegoInstancesList getInstancesList(XmlNode property)
        {

            int i, j;
            LegoObjects.LegoInstancesList instances = new LegoObjects.LegoInstancesList();
            LegoObjects.LegoInstance instance;
            string[] vals;
            string[] vals2;

            XmlNodeList insNodeList = property.SelectNodes(Const.STR_INSTANCE_TAG);

            for (i = 0; i < insNodeList.Count; i++)
            {
                //intervals = new List<TimeSeries.TimeInterval>();
                instance = new LegoObjects.LegoInstance(long.Parse(insNodeList[i].Attributes["o_id"].Value));

                vals = insNodeList[i].Attributes["tis"].Value.Split(',');

                for (j = 0; j < vals.Length; j++)
                {
                    // extract interval
                    vals2 = vals[j].Split('-');
                    instance.AddInterval(long.Parse(vals2[0]), long.Parse(vals2[1]));
                } // for intervals

                instances.Add(instance);

            } // for nodes
            instances.CalculateAvgPatternIntervals();
            return instances;

        } // getInstancesList


        /// <summary>
        /// get root node of XML index wekamatrixfile
        /// </summary>
        /// <param name="fileName">index wekamatrixfile name</param>
        /// <returns>root element</returns>
        public static XmlElement getRoot(string fileName)
        {
            XmlElement xmlRoot;
            XmlDocument xmdDoc = new XmlDocument();
            xmdDoc.Load(fileName);
            xmlRoot = xmdDoc.DocumentElement;
            return xmlRoot;

        } // getRoot


        /// <summary>
        /// create a set of files from a single Xml wekamatrixfile in order to control the files' sizes.
        /// </summary>
        /// <param name="filename">Xml wekamatrixfile to disassemble</param>
        public static void disAssembleXml(string filename)
        {

            int i;

            // dataset's name
            string orgFile = Methods.getFileNameNoExt(filename);
            string baseFileName = Methods.getFileNamePath(filename) + "\\" + orgFile;
            string curFileName;

            // index wekamatrixfile writer
            XmlTextWriter indexWriter = new XmlTextWriter(baseFileName + "-" + Const.STR_INDEX_FILE_NAME, System.Text.Encoding.Unicode);

            // current wekamatrixfile writer
            XmlTextWriter fileWriter;

            // read original wekamatrixfile
            XmlTextReader reader = new XmlTextReader(filename);

            // write wekamatrixfile name as root element
            indexWriter.WriteStartElement(repairFilename(orgFile));

            reader.Read();

            while (reader.Read())
            {
                if (reader.NodeType == XmlNodeType.Element)
                {
                    // getting  a first level property, create wekamatrixfile

                    // write found state to index wekamatrixfile
                    indexWriter.WriteStartElement(reader.Name);

                    reader.MoveToFirstAttribute();

                    curFileName = reader.Value.ToString();
                    curFileName = curFileName.Substring(0, curFileName.Length - 1);

                    // define new wekamatrixfile for found state
                    fileWriter = new XmlTextWriter(baseFileName + "-" + curFileName + ".xml", System.Text.Encoding.Unicode);

                    // write attributes
                    for (i = 0; i < reader.AttributeCount; i++)
                    {
                        reader.MoveToAttribute(i);
                        indexWriter.WriteAttributeString(reader.Name, reader.Value);
                    } // for attributes

                    // write wekamatrixfile name attribute
                    indexWriter.WriteAttributeString(Const.STR_FILENAME_ATTRIBUTE, orgFile + "-" + curFileName + ".xml");
                    reader.MoveToElement();
                    fileWriter.WriteNode(reader.ReadSubtree(), true);
                    indexWriter.WriteEndElement();
                    fileWriter.Close();
                } // if first level property
            }
            indexWriter.WriteEndElement();

            indexWriter.Close();
            reader.Close();

        } // diAssembleXml

        /// <summary>
        /// recursively 1st level property's data subtree, from an xml wekamatrixfile
        /// </summary>
        /// <param name="property">XML node to load, with subtrees</param>
        /// <returns>LegoProperty object, loaded with sub tree </returns>
        public static LegoObjects.LegoProperty recCreatePropertyData(XmlNode property)
        {
            int i;
            // get property data and create property
            LegoObjects.LegoProperty newProperty = getPropertyFromNode(property);

            // get next level properties
            LegoObjects.LegoPropertiesList lstNextLevelProperties = getNextPropertiesList(property, 1);

            // get current property instances list
            LegoObjects.LegoInstancesList lstInstances = getInstancesList(property);

            newProperty.Instances = lstInstances;

            newProperty.TIV = Statistics.Measures.getTIV(lstInstances);

            // stopping condition
            if (lstNextLevelProperties.PropertiesList.Count == 0)
            {
                newProperty.NextLevel = lstNextLevelProperties;
            } // if no sub tree
            else
            {
                XmlNodeList nodes = property.SelectNodes(Const.STR_TIRP_TAG);
                for (i = 0; i < nodes.Count; i++)
                {
                    lstNextLevelProperties.PropertiesList[i] = recCreatePropertyData(nodes[i]);
                    lstNextLevelProperties.PropertiesList[i].propIndex = i;
                }

                newProperty.NextLevel = lstNextLevelProperties;
            } // recursive call

            return newProperty;

        } // recCreatePropertyData

        /// <summary>
        /// Creates data for the given base property (level 1), 
        /// by loading data from its XML wekamatrixfile and converting it to Lego objects.
        /// </summary>
        /// <param name="results">LegoResults object to update</param>
        /// <param name="propertyIndex">property index in RootElements list</param>
        /// <returns>loaded LegoProperty</returns>
        public static LegoObjects.LegoProperty createPropertyData(LegoObjects.LegoResults results, int propertyIndex)
        {

            // get property wekamatrixfile name
            string fileName;
            XmlNode xmlProperty;
            LegoObjects.LegoProperty newProperty;

            if (results.RootElements.PropertiesList[propertyIndex].isLoaded)
            {
                // this is a property wekamatrixfile
                xmlProperty = results.Root;
            }
            else
            {
                string rootPath = Methods.getFileNamePath(results.strRootLocation);
                fileName = results.RootElementsFiles[propertyIndex];
                XmlDocument xmdDoc = new XmlDocument();
                // open wekamatrixfile for input
                xmdDoc.Load(rootPath + "\\" + fileName);

                // select first tirp - root
                xmlProperty = xmdDoc.SelectSingleNode(Const.STR_TIRP_TAG);
            } // normal index operation


            // create recursively the data tree
            newProperty = recCreatePropertyData(xmlProperty);

            newProperty.isLoaded = true;

            newProperty.propIndex = propertyIndex;

            return newProperty;

        } // createPropertyData

        #endregion XMLStructures


        #region KarmaStructures

        /// <summary>
        /// creates an intervals string as used in karma files
        /// </summary>
        /// <param name="intervals">list of intervals to create string for</param>
        /// <returns>karma intervals string</returns>
        public static string getKarmaIntervalsString(List<TimeSeries.TimeInterval> intervals)
        {
            string ans = "";
            int i;
            for (i = 0; i < intervals.Count; i++)
                ans += "[" + intervals[i].StartTime.ToString() + "-" + intervals[i].EndTime.ToString() + "]";
            return ans;

        } // getKarmaIntervalsString


        /// <summary>
        /// converts karma string representing time intervals list to xml structure
        /// </summary>
        /// <param name="strKarma">original karma string</param>
        /// <returns>xml string</returns>
        private static string convertIntervalsKarmaToXML(string strKarma)
        {
            string ans;
            ans = strKarma.Replace("][", ",");
            ans = ans.Replace(' ', '-');
            return ans.Substring(1, ans.Length - 2);
        } // ConvertIntervalsKarmaToXML

        /// <summary>
        /// write instances tags to an xml wekamatrixfile using a karma intervals line items
        /// </summary>
        /// <param name="writer">xml wekamatrixfile writer</param>
        /// <param name="vals">line items</param>
        private static void XMLWriteInstances(XmlTextWriter writer, string[] vals)
        {
            int i;
            int max = vals.Length;
            for (i = 0; i + 1 < max; i += 2)
            {
                writer.WriteStartElement(Const.STR_INSTANCE_TAG); // write ins tag
                writer.WriteAttributeString("o_id", vals[i]); // write states
                writer.WriteAttributeString("tis", convertIntervalsKarmaToXML(vals[i + 1]));
                writer.WriteEndElement();
            } // for

        } // XMLWriteInstances

        /// <summary>
        /// writes a tirp tag to an xml wekamatrixfile, given an array containing the values of attributes
        /// </summary>
        /// <param name="writer">xml wekamatrixfile writer</param>
        /// <param name="vals">array of values( level, states list, relations, V support, H support</param>
        private static void XMLWriteTIRP(XmlTextWriter writer, string[] vals)
        {

            writer.WriteStartElement(Const.STR_TIRP_TAG);
            writer.WriteAttributeString("prms", vals[1]); // write states
            writer.WriteAttributeString("rels", vals[2]); // write relation
            writer.WriteAttributeString("mhsup", vals[3]); // write horizontal support
            writer.WriteAttributeString("vsup", vals[4]); // write vertical support

        } //WriteTIRP


        /// <summary>
        /// writes a whole sub tree (of a single property) read from a karma wekamatrixfile 
        /// to a xml format wekamatrixfile
        /// </summary>
        /// <param name="kr">reader of the karma wekamatrixfile</param>
        /// <param name="writer">writer of the xml first level sub tree wekamatrixfile</param>
        /// <returns>empty array for end of wekamatrixfile, full array as the next first lvel property to load</returns>
        private static string[] writeKarmaSubTreeToXML(StreamReader sr, XmlTextWriter writer)
        {

            int curLevel = 1;
            int lastLevel = 1;
            string line;
            string[] vals;

            do
            {
                line = sr.ReadLine();
                if (line == null || line.Trim() == "")
                {
                    for (int i = 1; i <= lastLevel; i++)
                        writer.WriteEndElement();
                    return new string[0];
                } // end of wekamatrixfile
                vals = line.Split(' ');
                lastLevel = curLevel;
                curLevel = int.Parse(vals[0]);
                // close all open subtrees
                for (int i = curLevel; i <= lastLevel; i++)
                    writer.WriteEndElement();
                if (curLevel != 1)
                {
                    XMLWriteTIRP(writer, vals);
                    vals = (line = sr.ReadLine()).Split(' ');
                    XMLWriteInstances(writer, vals);
                } // write instances
            }
            while (curLevel != 1); // till next property
            return vals;

        } // WriteKarmaSubTreeToXML


        /// <summary>
        /// converts karma wekamatrixfile to an xml wekamatrixfile
        /// </summary>
        /// <param name="karmaFile">karma wekamatrixfile to convert</param>
        /// <param name="xmlFile">xml wekamatrixfile to save to</param>
        public static void convertKarmaToXML(string karmaFile, string xmlFile)
        {
            string line;
            string[] vals;


            // dataset's name
            string orgFile = Methods.getFileNameNoExt(xmlFile);
            string baseFileName = Methods.getFileNamePath(xmlFile) + "\\" + orgFile;
            string curFileName;

            // index wekamatrixfile writer
            XmlTextWriter indexWriter = new XmlTextWriter(baseFileName + "-" + Const.STR_INDEX_FILE_NAME, System.Text.Encoding.Unicode);

            // current wekamatrixfile writer
            XmlTextWriter fileWriter;

            // write wekamatrixfile name as root element
            indexWriter.WriteStartElement(repairFilename(orgFile));

            using (StreamReader sr = new StreamReader(karmaFile))
            {
                line = sr.ReadLine();
                vals = line.Split(' ');
                do
                {
                    curFileName = vals[1].Substring(0, vals[1].IndexOf('-'));

                    // define new wekamatrixfile for found state
                    fileWriter = new XmlTextWriter(baseFileName + "-" + curFileName + ".xml", System.Text.Encoding.Unicode);

                    Data.XMLWriteTIRP(fileWriter, vals);

                    // write 1st level sub tree
                    Data.XMLWriteTIRP(indexWriter, vals);
                    // write wekamatrixfile name attribute
                    indexWriter.WriteAttributeString(Const.STR_FILENAME_ATTRIBUTE, orgFile + "-" + curFileName + ".xml");
                    indexWriter.WriteEndElement();

                    sr.ReadLine(); // skip ; line

                    // recursively write sub tree (till level1)
                    vals = writeKarmaSubTreeToXML(sr, fileWriter);
                    fileWriter.Close();

                } while (vals != null && vals.Length > 0);

                indexWriter.WriteEndElement();
                indexWriter.Close();
            } // using 

        } // convertKarmaToXML

        /// <summary>
        /// creates an index wekamatrixfile for a given karma wekamatrixfile
        /// </summary>
        /// <param name="karmaFile">given karma wekamatrixfile to index</param>
        /// <returns>name of index wekamatrixfile created</returns>
        public static string createKarmaIndexFile(string karmaFile, string indexFile)
        {
            string line;
            string[] vals;
            //string indexFile = IndexFile.getIndexFileName(karmaFile);
            LegoObjects.LegoInstancesList lstInstances;
            using (KarmaFileReader sr = new KarmaFileReader(karmaFile))
            {
                using (StreamWriter sw = new StreamWriter(indexFile))
                {
                    while ((line = sr.getLine()) != null)
                    {
                        vals = line.Split(' ');
                        if (vals.Length == 5)
                        {
                            sw.WriteLine(line); // write pattern line
                            if (vals[0] != "1")
                            {
                                sr.readLine();
                                lstInstances = Data.getInstancesListFromKarma(sr);
                                lstInstances.CalculateAvgPatternIntervals();
                                sw.WriteLine(lstInstances.GetAvgPatternString());
                            }
                            else
                            {
                                sr.skipLine();
                                sw.WriteLine("-");
                            }
                        } // if writing record
                        else
                            sr.skipLine(); // skip ;
                    } // while
                } // using write
            } // using read

            return indexFile;

        } // CreateKarmaIndexFile


        /// <summary>
        /// given two cells of original splitted line of instances, a new instance
        /// will be returned
        /// </summary>
        /// <param name="id">entity id string (1st cell)</param>
        /// <param name="intervals">intervals string (2nd cell)</param>
        /// <returns>a new instance</returns>
        public static LegoObjects.LegoInstance getInstanceFromKarma(string id, string intervals)
        {

            LegoObjects.LegoInstance instNew = new LegoObjects.LegoInstance(long.Parse(id));

            intervals = intervals.Replace("][", " ");
            intervals = intervals.Substring(1, intervals.Length - 2);
            string[] vals = intervals.Split(' ');
            string[] times;
            for (int i = 0; i < vals.Length; i++)
            {
                times = vals[i].Split('-');
                instNew.AddInterval(long.Parse(times[0]), long.Parse(times[1]));
            } // for intervals
            return instNew;
        } // getInstanceFromKarma

        /// <summary>
        /// given a line of instances, instances list will be returned
        /// </summary>
        /// <param name="line">line of instances</param>
        /// <returns>list of instances</returns>
        private static LegoObjects.LegoInstancesList getInstancesListFromKarma(KarmaFileReader sr)
        {
            string word;
            LegoObjects.LegoInstancesList lstInstancesNew = new LegoObjects.LegoInstancesList();
            while ((word = sr.getWord()) != ";")
                lstInstancesNew.Add(getInstanceFromKarma(word.Trim(), sr.getWord().Trim()));
            sr.readLine();
            return lstInstancesNew;

        } // getInstancesListFromKarma

        /// <summary>
        /// given splitted karma property line, a new legoproperty will be returned
        /// </summary>
        /// <param name="vals">splitted karma property line</param>
        /// <returns>new legoproperty</returns>
        public static LegoObjects.LegoProperty parseKarmaPropertyString(string[] vals)
        {

            string[] props = vals[1].Split('-');

            return new LegoObjects.LegoProperty(int.Parse(props[props.Length - 2]), int.Parse(vals[3]), int.Parse(vals[4]), vals[2]);

        } // parseKarmaPropertyString
        public static LegoObjects.LegoProperty parseKarmaPropertyStringMergedFile(string[] vals)
        {

            string[] props = vals[1].Split('-');

            return new LegoObjects.LegoProperty(int.Parse(props[props.Length - 2]), int.Parse(vals[3]), int.Parse(vals[4]),double.Parse(vals[5]), int.Parse(vals[6]), int.Parse(vals[7]), double.Parse(vals[8]), vals[2]);

        } // parseKarmaPropertyString

        /// <summary>
        /// used for saving last values for next property feed
        /// </summary>
        private static string[] strVals;

        /// <summary>
        /// given a loaded karma wekamatrixfile, a whole first level sub tree of data will be returned
        /// if not end of wekamatrixfile, strVals will save the next property's values
        /// </summary>
        /// <param name="kr">karma wekamatrixfile stream reader </param>
        /// <returns>next level sub tree</returns>
        public static LegoObjects.LegoPropertiesList getSubTreeFromKarmaFile(KarmaFileReader sr, bool isMerged)
        {
            string line;
            string[] vals;
            int CurrentLevel = 1;
            LegoObjects.LegoProperty propTemp;
            LegoObjects.LegoPropertiesList lstTemp;
            LegoObjects.LegoPropertiesList[] lstLevels = new LegoObjects.LegoPropertiesList[20];
            lstLevels[0] = new LegoObjects.LegoPropertiesList(false); // first level's next level


            line = sr.getLine();
            if (line == null)
                return new LegoObjects.LegoPropertiesList(false);

            line = line.Trim();
            while (line != null && line != "")
            {
                vals = line.Split(' ');
                CurrentLevel = int.Parse(vals[0]);
                if (CurrentLevel == 1)
                {
                    strVals = vals;
                    return lstLevels[0];
                } // finished sub tree
                if (!isMerged)
                    propTemp = parseKarmaPropertyString(vals);
                else
                    propTemp = parseKarmaPropertyStringMergedFile(vals);

                lstTemp = new LegoObjects.LegoPropertiesList(false);
                propTemp.Instances = getInstancesListFromKarma(sr);
                propTemp.Instances.CalculateAvgPatternIntervals();
                propTemp.TIV = Statistics.Measures.getTIV(propTemp.Instances);
                propTemp.NextLevel = lstTemp;
                propTemp.propIndex = lstLevels[CurrentLevel - 2].PropertiesList.Count;
                lstLevels[CurrentLevel - 2].Add(propTemp);
                lstLevels[CurrentLevel - 1] = lstTemp;
                line = sr.getLine();

            } // while

            // reached end of wekamatrixfile, notify calling function
            strVals = new string[0];
            return lstLevels[0];

        } // getSubTreeFromKarmFile



        /// <summary>
        /// given a loaded karma wekamatrixfile, a whole first level sub tree of data will be returned
        /// if not end of wekamatrixfile, strVals will save the next property's values
        /// </summary>
        /// <param name="kr">karma wekamatrixfile stream reader </param>
        /// <returns>next level sub tree</returns>
        public static LegoObjects.LegoPropertiesList getSubTreeFromKarmaFileNoInstances(KarmaFileReader sr)
        {
            string line;
            string[] vals;
            int CurrentLevel = 1;
            LegoObjects.LegoProperty propTemp;
            LegoObjects.LegoPropertiesList lstTemp;
            LegoObjects.LegoPropertiesList[] lstLevels = new LegoObjects.LegoPropertiesList[20];
            lstLevels[0] = new LegoObjects.LegoPropertiesList(false); // first level's next level


            line = sr.getLine();
            if (line == null)
                return new LegoObjects.LegoPropertiesList(false);

            line = line.Trim();
            while (line != null && line != "")
            {
                vals = line.Split(' ');
                CurrentLevel = int.Parse(vals[0]);
                if (CurrentLevel == 1)
                {
                    strVals = vals;
                    return lstLevels[0];
                } // finished sub tree
                propTemp = parseKarmaPropertyString(vals);
                lstTemp = new LegoObjects.LegoPropertiesList(false);
                sr.skipLine();
                propTemp.NextLevel = lstTemp;
                propTemp.propIndex = lstLevels[CurrentLevel - 2].PropertiesList.Count;
                lstLevels[CurrentLevel - 2].Add(propTemp);
                lstLevels[CurrentLevel - 1] = lstTemp;
                line = sr.getLine();

            } // while

            // reached end of wekamatrixfile, notify calling function
            strVals = new string[0];
            return lstLevels[0];

        } // getSubTreeFromKarmFile



        /// <summary>
        /// used in order to split a given karma file into sub trees files.
        /// The index file will contain references to the sub trees files.
        /// </summary>
        /// <param name="karmafilename">given karma file</param>
        /// <param name="outputfolder">folder to save sub trees files in</param>
        /// <param name="datasetname">files names prefix</param>
        public static void splitKarmaFile(string karmafilename, string outputfolder, string datasetname)
        {
            string line, curfilename, curproperty;
            LegoObjects.LegoPattern pattern;
            string[] vals;
            using (KarmaFileReader kr = new KarmaFileReader(karmafilename))
            {
                using (StreamWriter indexsw = new StreamWriter(outputfolder + "\\" + datasetname + "-Index.karmac"))
                {
                    line = kr.getLine();
                    while (line != null && line.Trim() != "")
                    {
                        vals = line.Split(' ');
                        if (vals[0] == "1") // first level
                        {
                            curproperty = vals[1].Substring(0, vals[1].LastIndexOf('-'));
                            curfilename = outputfolder + "\\" + datasetname + "-" + curproperty + ".karmac";
                            indexsw.WriteLine(line); // write property info
                            indexsw.WriteLine(datasetname + "-" + curproperty + ".karmac"); // write filename for karma sub tree

                            using (StreamWriter propsw = new StreamWriter(curfilename))
                            {
                                kr.skipLine(); // skip ; line
                                while ((line = kr.getLine()) != null && line.Split(' ')[0] != "1")
                                {
                                    propsw.WriteLine(line);
                                    kr.copyLine(propsw);
                                } // write property sub tree
                            } // using property writer

                        } // if first level
                    } // while reading karma file

                } // using writer

            } // using reader
        } // splitKarmaFile

        /// <summary>
        /// used in order to merge a given karma file into sub trees files.
        /// The index file will contain references to the sub trees files.
        /// </summary>
        /// <param name="karmaFileNameClass0">given karma file</param>
        /// <param name="karmaFileNameClass1">given karma file</param>
        /// <param name="outputFolder">folder to save sub trees files in</param>
        /// <param name="outFileName">files names prefix</param>
        public static void Merge2ClassesKarmaFiles(string karmaFileNameClass0, string karmaFileNameClass1, string outputFolder, string outFileName)
        {
            Dictionary<string, string[]> class0PatternsDictionary = new Dictionary<string, string[]>();
            string line;
            string[] vals;
            string mergeFileName = outputFolder + "\\" + outFileName + ".karma";


            using (KarmaFileReader kr = new KarmaFileReader(karmaFileNameClass0))
            {
                line = kr.getLine();
                while (line != null && line.Trim() != "")
                {
                    vals = line.Split(' ');
                    string keyVals = "";
                    for (int i = 0; i < vals.Length - 2; i++)
                    {
                        keyVals += vals[i] + " ";
                    }
                    string supportsValues = vals[vals.Length - 2] + " " + vals[vals.Length - 1];
                    class0PatternsDictionary.Add(keyVals, new string[] { supportsValues, kr.getLine() });
                }
            }
            using (StreamWriter mergeFile = new StreamWriter(mergeFileName))
            {
                using (KarmaFileReader kr = new KarmaFileReader(karmaFileNameClass1))
                {

                    line = kr.getLine();
                    while (line != null && line.Trim() != "")
                    {
                        vals = line.Split(' ');
                        string keyVals = "";
                        for (int i = 0; i < vals.Length - 2; i++)
                        {
                            keyVals += vals[i] + " ";
                        }
                        string supportsValues = vals[vals.Length - 2] + " " + vals[vals.Length - 1];

                        if (class0PatternsDictionary.ContainsKey(keyVals))
                        {

                            mergeFile.WriteLine(keyVals + class0PatternsDictionary[keyVals][0] + " " + supportsValues);
                            mergeFile.WriteLine(class0PatternsDictionary[keyVals][1] + kr.getLine() + ";");

                            class0PatternsDictionary.Remove(keyVals);
                        }
                        else
                        {

                            mergeFile.WriteLine(keyVals + "0 0 " + supportsValues);
                            mergeFile.WriteLine(kr.getLine() + ";");


                        }
                    }
                }

                foreach (string key in class0PatternsDictionary.Keys)
                {

                    mergeFile.WriteLine(class0PatternsDictionary[key] + class0PatternsDictionary[key][0] + " 0 0");
                    mergeFile.WriteLine(class0PatternsDictionary[key][1]);

                }
            }
        }


        /// <summary>
        /// load a karma sub tree to a LegoPropertiesList object.
        /// </summary>
        /// <param name="filename">karma sub tree filename</param>
        /// <returns>LegoPropertiesList from given file </returns>
        public static LegoObjects.LegoPropertiesList loadKarmaSubTree(byte[] byteArr, bool isMerged)
        {
            return getSubTreeFromKarmaFile(new KarmaFileReader(byteArr), isMerged);
        }


        /// <summary>
        /// load a karma sub tree to a LegoPropertiesList object.
        /// </summary>
        /// <param name="filename">karma sub tree filename</param>
        /// <returns>LegoPropertiesList from given file </returns>
        public static LegoObjects.LegoPropertiesList loadKarmaSubTreeNoInstances(string filename)
        {
            return getSubTreeFromKarmaFileNoInstances(new KarmaFileReader(filename));
        }



        /// <summary>
        /// given a karma wekamatrixfile name, all data will be loaded into a properties list
        /// </summary>
        /// <param name="karmaFile">karma wekamatrixfile name</param>
        /// <returns>properties list</returns>
        public static LegoObjects.LegoPropertiesList loadKarmaFileDirect(byte[] byteArr)
        {

            int i = 0;

            string line;

            LegoObjects.LegoPropertiesList lstData = new LegoObjects.LegoPropertiesList(true);
            LegoObjects.LegoProperty property;

            using (KarmaFileReader kr = new KarmaFileReader(byteArr))
            {
                line = kr.getLine();
                strVals = line.Split(' ');
                do
                {
                    property = parseKarmaPropertyString(strVals);

                    kr.skipLine(); // skip ; line

                    // recursively load sub tree (till level1)
                    property.NextLevel = getSubTreeFromKarmaFile(kr, false);

                    property.isLoaded = true;

                    property.propIndex = i;

                    i++;

                    lstData.PropertiesList.Add(property);

                } while (strVals != null && strVals.Length > 0);

            } // using 

            return lstData;

        } // LoadKarmaFileDirect


        /// <summary>
        /// an object used to hold data of vertical support and index in wekamatrixfile
        /// </summary>
        class PointIndex
        {

            public long index;
            public int vs;

            public PointIndex(long index1, int vs1)
            {
                index = index1;
                vs = vs1;
            }

        } // PointIndex


        /// <summary>
        /// given a list of PointIndexes, the one with the highest vertical support will be returned and be removed from the list.
        /// </summary>
        /// <param name="list">list of points</param>
        /// <returns>winning point</returns>
        private static PointIndex findRemoveMaximal(List<PointIndex> list)
        {
            PointIndex ans;
            int i;
            int max = 0;
            for (i = 1; i < list.Count; i++)
                if (list[i].vs > list[max].vs)
                    max = i;

            ans = list[max];
            list.RemoveAt(max);
            return ans;
        } // findRemoveMaximal


        /// <summary>
        /// given a list of PointIndex and maximal number of features, a list of indexes holding the highest patterns by their vertical support
        /// will be returned. indexes list is sorted, in order to write to wekamatrixfile.
        /// </summary>
        /// <param name="list">list of pointindex </param>
        /// <param name="features">maximum number of features to keep</param>
        /// <returns>list of line indexes in wekamatrixfile</returns>
        private static long[] getBestFeaturesIndexes(List<PointIndex> list, int features)
        {
            //int i = 0;
            List<long> lstIndexes = new List<long>();
            while (list.Count > 0 && features > 0)
            {
                lstIndexes.Add(findRemoveMaximal(list).index);
                features--;
            } // while adding filtercount.
            lstIndexes.Sort();
            return lstIndexes.ToArray();
        } // getBestFeaturesIndexes

        /// <summary>
        /// given a list of line indexes to write, a new wekamatrixfile will be created containing only indexed patterns (and their instances lists)
        /// </summary>
        /// <param name="oldfile">wekamatrixfile to copy from</param>
        /// <param name="newfile">new wekamatrixfile to create</param>
        /// <param name="indexes">list of indexes</param>
        private static void writeToKarmaFileByIndexes(string oldfile, string newfile, long[] indexes)
        {

            long index = 0;
            int i = 0;
            string line;

            using (StreamReader sr = new StreamReader(oldfile))
            {

                using (StreamWriter sw = new StreamWriter(newfile))
                {

                    while ((line = sr.ReadLine()) != null && i < indexes.Length)
                    {
                        if (indexes[i] == index)
                        {
                            sw.WriteLine(line); // write tirp
                            sw.WriteLine(sr.ReadLine()); // write instances
                            i++;
                        }
                        else
                            sr.ReadLine();
                        index += 2;
                    } // while reading and adding

                } // using writer

            } // using reader

        } // writeToKarmaFileByIndexes

        /// <summary>
        /// given a karma wekamatrixfile, a list of patterns' indexes will be returned, companied with the vertical support value
        /// </summary>
        /// <param name="filename">karma wekamatrixfile name</param>
        /// <returns>list of indexes and vertical support</returns>
        private static List<PointIndex> getPatternsIndexes(string filename)
        {
            List<PointIndex> lstAns = new List<PointIndex>();
            string line;
            int i = 0;

            using (StreamReader sr = new StreamReader(filename))
            {

                while ((line = sr.ReadLine()) != null)
                {
                    lstAns.Add(new PointIndex(i, int.Parse(line.Split(' ')[4])));
                    sr.ReadLine();
                    i += 2;
                }

            } // using
            return lstAns;
        } // getPatternsIndexes

        /// <summary>
        /// given a working folder containing karma files, this automated function will create filtered files for all karma files,
        /// containing only filtercount (or all, if patterns count is smaller) patterns by the highest vertical support values. 
        /// </summary>
        /// <param name="basefolder">working folder</param>
        /// <param name="filtercount">maximum number of patterns to keep</param>
        public static void findBestFeatures(string basefolder, int filtercount)
        {

            List<PointIndex> lstPoints;
            long[] indexes;
            string[] files = System.IO.Directory.GetFiles(basefolder);
            for (int i = 0; i < files.Length; i++)
            {

                if (files[i].IndexOf("karma") != -1)
                {

                    lstPoints = getPatternsIndexes(files[i]);
                    indexes = getBestFeaturesIndexes(lstPoints, filtercount);
                    writeToKarmaFileByIndexes(files[i], basefolder + "\\" + Methods.getFileNameNoExt(files[i]) + "Best" + indexes.Length.ToString() + ".karma", indexes);
                } // handle wekamatrixfile

            } // for files


        } // findBestFeatures



        /// <summary>
        /// given a karma wekamatrixfile, and entity to work by, a new filtered wekamatrixfile will be created named by function parameters.
        /// new wekamatrixfile will include only patterns apearing over minimalusersupport times in user's data, and their vertical support is no higher than maximalverticalsupport.
        /// 
        /// </summary>
        /// <param name="filename">given karma wekamatrixfile to maxgaps</param>
        /// <param name="basefolder">working folder</param>
        /// <param name="entities">array of entities' id numbers</param>
        /// <param name="entityindex">index in array of entities id numbers to use as current entity id</param>
        /// <param name="minimalusersupport">minimal horizontal support to force</param>
        /// <param name="maximalverticalsupport">maximal vertical support to force</param>
        /// <param name="diventityID">divide entity id by - used to group entities</param>
        /// <returns>new wekamatrixfile's name</returns>
        public static string filterKarmaFile(string filename, string basefolder, int[] entities, int entityindex, int minimalusersupport, int maximalverticalsupport, int diventityID)
        {
            string line;
            string[] vals;
            int[] entitiescounters;
            LegoObjects.LegoInstancesList lstInstances;
            string filenamenew = basefolder + "\\" + Methods.getFileNameNoExt(filename) + "Entity" + entities[entityindex].ToString() + "Filter" + minimalusersupport.ToString() + "-" + maximalverticalsupport.ToString() + ".karma";
            using (KarmaFileReader sr = new KarmaFileReader(filename))
            {

                using (StreamWriter sw = new StreamWriter(filenamenew))
                {
                    while ((line = sr.getLine()) != null)
                    {
                        vals = line.Split(' ');
                        if (int.Parse(vals[0]) == 1) // if level 1
                            sr.skipLine();
                        else if (int.Parse(vals[4]) > maximalverticalsupport) // vertical support too high
                            sr.skipLine();
                        else
                        {
                            lstInstances = getInstancesListFromKarma(sr);
                            entitiescounters = LegoObjects.LegoInstancesList.countInstancesPerUser(lstInstances, entities, diventityID);

                            if (entitiescounters[entityindex] >= minimalusersupport)
                            {
                                sw.WriteLine(line);
                                // ************ add : place pointer before previous line (which is the instances line)
                            }
                        }

                    } // while reading

                }// using writer
            } // using reader     
            return filenamenew;

        } // filterKarmaFile


        #endregion KarmaStructures

    } // class Data

    /// <summary>
    /// Used for searching the patterns, this will hold all the necessary data for searching, 
    /// without instances data.
    /// </summary>
    public class BasicPattern
    {
        public List<long> lstProperties;
        public string Relations;
        public int Level;
        public long VerticalSupport;
        public long HorizontalSupport;
        public LegoObjects.LegoInstance AveragePattern;

        public BasicPattern(string properties, string rels, long vsupp, long hsupp, LegoObjects.LegoInstance avgPattern)
        {
            lstProperties = new List<long>();
            string[] vals = properties.Split('-');
            for (int i = 0; i < vals.Length; i++)
                if (vals[i].Trim() != "")
                    lstProperties.Add(long.Parse(vals[i].Trim()));
            VerticalSupport = vsupp;
            HorizontalSupport = hsupp;
            Level = vals.Length - 1;
            Relations = rels;
            AveragePattern = avgPattern;
        } // basic constructor

        /// <summary>
        /// returns a string representing the pattern's properties as displayed in the search results list
        /// </summary>
        /// <param name="cnv">States converter used to translate state ID to its name</param>
        /// <returns>String representing the pattern's properties</returns>
        public string getPropertiesString(StatesConverter cnv)
        {
            string ans = "";

            for (int i = 0; i < lstProperties.Count; i++)
            {
                ans += cnv.getLabel((int)lstProperties[i]);
                if (i < lstProperties.Count - 1)
                    ans += " - ";
            } // for properties

            return ans;

        } // GetPropertiesString

        /// <summary>
        /// returns the pattern's string, as written in the original karma wekamatrixfile ( and index wekamatrixfile)
        /// </summary>
        /// <returns></returns>
        public string getPatternString()
        {
            int level = lstProperties.Count;
            string ans = level.ToString() + " " +
                         Methods.Arrays.getArrayString(lstProperties.ToArray()) + " " +
                         Relations + " " +
                         HorizontalSupport.ToString() + " " +
                         VerticalSupport.ToString();
            return ans;

        } // GetPatternSTring

    } // class BasicPattern

    /// <summary>
    /// holds a list of basic patterns
    /// </summary>
    public class BasicPatternsList
    {
        List<BasicPattern> lstPatterns;

        public BasicPatternsList()
        {
            lstPatterns = new List<BasicPattern>();
        } // basic constructor

        public void add(BasicPattern pattern)
        {
            lstPatterns.Add(pattern);
        } // Add

        public long Count()
        {
            return lstPatterns.Count;
        } // Count

        public BasicPattern at(int index)
        {
            return lstPatterns[index];
        } // At

        /// <summary>
        /// writes the patterns to an index wekamatrixfile
        /// </summary>
        /// <param name="filename"></param>
        public void writeIndexFile(string filename)
        {
            IndexFile newIndex = new IndexFile(filename);
            newIndex.fill(this);
        } // WriteIndexFile



    } // class BasicPatternsList

    /// <summary>
    /// manages the search parameters, including checking validity 
    /// </summary>
    public class SearchParameters
    {

        public long[] StartsWith;
        public long[] EndsWith;
        public long[] Contains;
        public long VSuppMin;
        public long VSuppMax;
        public long HSuppMin;
        public long HSuppMax;
        public long LevMin;
        public long LevMax;


        public SearchParameters(long[] pStartsWith, long[] pEndsWith, long[] pContains, long pVSuppMin, long pVSuppMax, long pHSuppMin, long pHSuppMax, long levMin, long levMax)
        {
            StartsWith = pStartsWith;
            EndsWith = pEndsWith;
            Contains = pContains;
            VSuppMin = pVSuppMin;
            VSuppMax = pVSuppMax == -1 ? long.MaxValue : pVSuppMax;
            HSuppMin = pHSuppMin;
            HSuppMax = pHSuppMax == -1 ? long.MaxValue : pHSuppMax;
            LevMin = levMin;
            LevMax = levMax == -1 ? long.MaxValue : levMax;
        } // basic constructor


        public bool checkHSupp(long tocheck)
        {
            return tocheck <= HSuppMax && tocheck >= HSuppMin;
        } // checkHSupp

        public bool checkVSupp(long tocheck)
        {
            return tocheck <= VSuppMax && tocheck >= VSuppMin;
        } // checkVSupp

        public bool checkLevel(long tocheck)
        {
            return tocheck <= LevMax && tocheck >= LevMin;
        } // checkLevel

        public bool checkStart(string pattern)
        {
            string[] vals = pattern.Split('-');
            return StartsWith.Length != 0 ? Methods.Arrays.isMember(long.Parse(vals[0]), StartsWith) != -1 : true;
        } // checkStart

        public bool checkMiddle(string pattern)
        {
            if (Contains.Length == 0) return true;
            string[] vals = pattern.Split('-');
            bool ans = false;
            int i = 1;
            while (i <= vals.Length - 3 && !ans)
                if (Methods.Arrays.isMember(long.Parse(vals[i++]), Contains) != -1)
                    ans = true;
            return ans;
        } // checkMiddle

        public bool checkEnd(string pattern)
        {
            string[] vals = pattern.Split('-');
            return EndsWith.Length != 0 ? Methods.Arrays.isMember(long.Parse(vals[vals.Length - 2]), EndsWith) != -1 : true;
        } // checkEnd


    } // class SearchParameters

    /// <summary>
    /// Manages an index wekamatrixfile, including loading and saving
    /// </summary>
    public class IndexFile
    {

        public string FileName;
        public int maxDepth;

        public IndexFile(string fileName)
        {
            FileName = fileName;
            maxDepth = 0;
        } // basic constructor

        /// <summary>
        /// searches through the index wekamatrixfile, looking for patterns matching the given search parameters
        /// </summary>
        /// <param name="opt">Search parameters object to use as a search maxgaps</param>
        /// <returns>list of basic patterns matching the search maxgaps</returns>
        public BasicPatternsList search(SearchParameters opt)
        {

            BasicPatternsList list = new BasicPatternsList();
            LegoObjects.LegoInstance instAvg;

            string line;
            string[] vals;

            using (StreamReader sr = new StreamReader(FileName))
            {
                while ((line = sr.ReadLine()) != null)
                {
                    vals = line.Split(' ');
                    if (opt.checkHSupp(long.Parse(vals[3])) &&
                        opt.checkVSupp(long.Parse(vals[4])) &&
                        opt.checkLevel(long.Parse(vals[0])) &&
                        opt.checkStart(vals[1]) &&
                        opt.checkMiddle(vals[1]) &&
                        opt.checkEnd(vals[1]))
                    {
                        if ((line = sr.ReadLine()).Trim() != "-")
                            instAvg = Data.getInstanceFromKarma("0", line);
                        else
                            instAvg = null;
                        list.add(new BasicPattern(vals[1], vals[2], long.Parse(vals[4]), long.Parse(vals[3]), instAvg));
                        if (vals[1].Split('-').Length - 1 > maxDepth)
                            maxDepth = vals[1].Split('-').Length - 1;
                    }
                    else
                        sr.ReadLine(); // skip this pattern's avg instance
                } // while reading

            } // using reader

            return list;

        } // search

        public static string getIndexFileName(string karmaFile)
        {
            return Methods.getFileNamePath(karmaFile) + "\\" + Methods.getFileNameNoExt(karmaFile) + "-index.kindex";
        } // GetIndexFileName


        /// <summary>
        /// saves a list of basic patterns to an index wekamatrixfile
        /// </summary>
        /// <param name="list"></param>
        public void fill(BasicPatternsList list)
        {

            int i;
            using (StreamWriter sw = new StreamWriter(FileName))
            {

                for (i = 0; i < list.Count(); i++)
                {

                    sw.WriteLine(list.at(i).getPatternString());
                    if (list.at(i).AveragePattern != null)
                        sw.WriteLine(Data.getKarmaIntervalsString(list.at(i).AveragePattern.Intervals));
                    else
                        sw.WriteLine("-");

                } // for list of patterns

            } // using writer

        } // Fill


    } // class IndexFile






} // namespace
