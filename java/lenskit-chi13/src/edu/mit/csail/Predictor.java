package edu.mit.csail;

import java.io.File;
import java.util.HashSet;
import java.util.Set;

import org.grouplens.lenskit.GlobalItemRecommender;
import org.grouplens.lenskit.GlobalItemScorer;
import org.grouplens.lenskit.GlobalRatingPredictor;
import org.grouplens.lenskit.ItemRecommender;
import org.grouplens.lenskit.RatingPredictor;
import org.grouplens.lenskit.Recommender;
import org.grouplens.lenskit.RecommenderBuildException;
import org.grouplens.lenskit.RecommenderEngine;
import org.grouplens.lenskit.baseline.BaselinePredictor;
import org.grouplens.lenskit.baseline.ItemMeanPredictor;
import org.grouplens.lenskit.baseline.ItemUserMeanPredictor;
import org.grouplens.lenskit.collections.ScoredLongList;
import org.grouplens.lenskit.core.LenskitRecommenderEngineFactory;
import org.grouplens.lenskit.data.dao.SimpleFileRatingDAO;
import org.grouplens.lenskit.knn.item.ItemItemGlobalRecommender;
import org.grouplens.lenskit.knn.item.ItemItemGlobalScorer;
import org.grouplens.lenskit.knn.item.ItemItemRatingPredictor;
import org.grouplens.lenskit.knn.item.ItemItemRecommender;
import org.grouplens.lenskit.knn.item.ItemSimilarity;
import org.grouplens.lenskit.knn.item.NeighborhoodScorer;
import org.grouplens.lenskit.knn.item.SimilaritySumNeighborhoodScorer;
import org.grouplens.lenskit.knn.item.WeightedAverageNeighborhoodScorer;
import org.grouplens.lenskit.knn.params.NeighborhoodSize;

import org.grouplens.lenskit.params.Damping;
import org.grouplens.lenskit.transform.normalize.BaselineSubtractingUserVectorNormalizer;
import org.grouplens.lenskit.transform.normalize.MeanVarianceNormalizer;
import org.grouplens.lenskit.transform.normalize.UserVectorNormalizer;
import org.grouplens.lenskit.transform.normalize.VectorNormalizer;
import org.grouplens.lenskit.vectors.similarity.PearsonCorrelation;
import org.grouplens.lenskit.vectors.similarity.VectorSimilarity;

public class Predictor {
	
	@SuppressWarnings("unchecked")
	public static void main(String[] args){
		try {
			LenskitRecommenderEngineFactory factory = new LenskitRecommenderEngineFactory();
			File f = new File("/Users/anantb/data_lenskit.txt");
			factory.setDAOFactory(new SimpleFileRatingDAO.Factory(f, "\t"));
			/* configure a normalizer and baseline predictor */
			factory.bind(UserVectorNormalizer.class)
		       .to(BaselineSubtractingUserVectorNormalizer.class);
			factory.bind(BaselinePredictor.class)
			       .to(ItemMeanPredictor.class);
			factory.bind(GlobalItemScorer.class).to(ItemItemGlobalScorer.class);
			factory.bind(GlobalItemRecommender.class).to(ItemItemGlobalRecommender.class);
			RecommenderEngine engine = factory.create();
			/* get the and use the recommender */
			Recommender rec = engine.open();
			GlobalItemRecommender grec = rec.getGlobalItemRecommender();
			Set<Long> input_items = new HashSet<Long>();
			input_items.add(501460L);
			ScoredLongList recommendations = grec.globalRecommend(input_items, 10);
			long items[] = new long[10];
			double scores[] = new double[10];
			recommendations.getElements(0, items, scores, 0, 10);
			for(int i=0; i< 10; i++){
				System.out.println(items[i] + ":" + scores[i]);
			}
			
		} catch (RecommenderBuildException e) {
			e.printStackTrace();
		}catch(Exception e){
			e.printStackTrace();
		}
		

		
		
		
	}

}
