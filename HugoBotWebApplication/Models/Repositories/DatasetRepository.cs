using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace HugoBotWebApplication.Models.Repositories
{
    public class DatasetRepository : Repository<Dataset>
    {
       
        public DatasetRepository(ApplicationDbContext context) : base(context)
        {

        }
        public List<Dataset> GetByName(string name)
        {
            return DbSet.Where(dataset => dataset.DatasetName.Contains(name)).ToList();
        }

        public int GetNextId()
        {
            int nextDatasetId = 0;
            try
            {
                nextDatasetId = DbSet.Max(dataset => dataset.DatasetID);
                nextDatasetId += 1;
            }
            catch
            {

            }

            return nextDatasetId;
        }
        public Dataset GetByPath(string path)
        {
            List<Dataset> datasetByPath = DbSet.Where(dataset => dataset.Path.Equals(path)).ToList();
            if (datasetByPath.Count == 0)
                return null;
            return datasetByPath[0];
        }
    }
}