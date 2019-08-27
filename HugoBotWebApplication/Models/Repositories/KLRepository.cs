using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace HugoBotWebApplication.Models.Repositories
{
    public class KLRepository : Repository<KarmaLego>
    {

        public KLRepository(ApplicationDbContext context) : base(context)
        {

        }

        public int GetNextId()
        {
            int nextKLId = 0;
            try
            {
                nextKLId = DbSet.Max(karmalego => karmalego.KarmaLegoID);
                nextKLId += 1;
            }
            catch
            {

            }

            return nextKLId;
        }
    }
}