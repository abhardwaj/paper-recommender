package edu.mit.csail;

import java.io.File;

import org.grouplens.lenskit.ItemRecommender;
import org.grouplens.lenskit.RatingPredictor;
import org.grouplens.lenskit.Recommender;
import org.grouplens.lenskit.RecommenderBuildException;
import org.grouplens.lenskit.RecommenderEngine;
import org.grouplens.lenskit.baseline.BaselinePredictor;
import org.grouplens.lenskit.baseline.ItemUserMeanPredictor;
import org.grouplens.lenskit.collections.ScoredLongList;
import org.grouplens.lenskit.core.LenskitRecommenderEngineFactory;
import org.grouplens.lenskit.data.dao.SimpleFileRatingDAO;
import org.grouplens.lenskit.knn.item.ItemItemRatingPredictor;
import org.grouplens.lenskit.knn.item.ItemItemRecommender;
import org.grouplens.lenskit.knn.item.NeighborhoodScorer;
import org.grouplens.lenskit.knn.item.WeightedAverageNeighborhoodScorer;

import org.grouplens.lenskit.transform.normalize.BaselineSubtractingUserVectorNormalizer;
import org.grouplens.lenskit.transform.normalize.UserVectorNormalizer;

public class Predictor {
	
	public static void main(String[] args){
		try {
			LenskitRecommenderEngineFactory factory = new LenskitRecommenderEngineFactory();
			File f = new File("/Users/anantb/data_lenskit.txt");
			factory.setDAOFactory(new SimpleFileRatingDAO.Factory(f, "\t"));
			/* configure a normalizer and baseline predictor */
			factory.bind(UserVectorNormalizer.class)
		       .to(BaselineSubtractingUserVectorNormalizer.class);
			factory.bind(BaselinePredictor.class)
			       .to(ItemUserMeanPredictor.class);
			factory.bind(RatingPredictor.class).to(ItemItemRatingPredictor.class);
			//factory.bind(NeighborhoodScorer.class).to(SimilaritySumNeighborhoodScorer.class);
			factory.bind(NeighborhoodScorer.class).to(WeightedAverageNeighborhoodScorer.class);
			factory.bind(ItemRecommender.class).to(ItemItemRecommender.class);
			RecommenderEngine engine = factory.create();
			/* get the and use the recommender */
			Recommender rec = engine.open();
			ItemRecommender irec = rec.getItemRecommender();
			ScoredLongList recommendations = irec.recommend(122, 10);
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
