using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace HugoBotWebApplication.Models.Repositories
{
    public class DiscretizationRepository : Repository<Discretization>
    {
       
        public DiscretizationRepository(ApplicationDbContext context):base(context)
        {
            
        }
        public List<Discretization> GetByName(string name)
        {
            return DbSet.Where(discretization => discretization.Dataset.DatasetName.Contains(name)).ToList();
        }

        public int GetNextId()
        {
            int nextDiscretizationId = 0;
            try
            {
                nextDiscretizationId = DbSet.Max(discretization => discretization.DiscretizationID);
                nextDiscretizationId += 1;
            }
            catch
            {

            }

            return nextDiscretizationId;
        }
    }
}