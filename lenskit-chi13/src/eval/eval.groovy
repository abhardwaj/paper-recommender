import org.grouplens.lenskit.eval.data.crossfold.RandomOrder

import org.grouplens.lenskit.knn.params.*
import org.grouplens.lenskit.knn.item.*
import org.grouplens.lenskit.knn.user.*

import org.grouplens.lenskit.transform.normalize.*

import edu.mit.csail.ExtendedItemUserMeanPredictor

def chi2013 = crossfold {
   source csvfile("${config.dataDir}/chi2013/data.txt") {
      delimiter "\t"
      domain {
         minimum 1.0
         maximum 5.0
         precision 0.25
      }
   }
   test "${config.dataDir}/chi2013-crossfold/test.%d.csv"
   train "${config.dataDir}/chi2013-crossfold/train.%d.csv" 
}

def itemitem = algorithm("ItemItem") {
    // use the item-item rating predictor with a baseline and normalizer
    bind RatingPredictor to ItemItemRatingPredictor
    bind BaselinePredictor to ItemUserMeanPredictor
    bind UserVectorNormalizer to BaselineSubtractingUserVectorNormalizer

    // retain 500 neighbors in the model, use 30 for prediction
    set ModelSize to 10
    set NeighborhoodSize to 5

    // apply some Bayesian smoothing to the mean values
    within(ItemUserMeanPredictor) {
        set Damping to 25.0d
    }
}

def useruser = algorithm("UserUser") {
    // use the user-user rating predictor
    bind RatingPredictor to UserUserRatingPredictor
    bind BaselinePredictor to ItemUserMeanPredictor
    bind VectorNormalizer to MeanVarianceNormalizer

    // use 30 neighbors for predictions
    set NeighborhoodSize to 5

    // override normalizer within the neighborhood finder
    // this makes it use a different normalizer (subtract user mean) for computing
    // user similarities
    within(NeighborhoodFinder) {
        bind UserVectorNormalizer to BaselineSubtractingUserVectorNormalizer
        // override baseline to use user mean
        bind BaselinePredictor to UserMeanPredictor
    }

    // and apply some Bayesian damping to the baseline
    within(ItemUserMeanPredictor) {
        set Damping to 25.0d
    }
}

def extended = algorithm("ExtendedItemUserMean") {
	bind RatingPredictor to ExtendedItemUserMeanPredictor
}

dumpGraph {
	output "${config.analysisDir}/extended.gv"
	algorithm extended
}

trainTest {
	dataset chi2013

	// Three different types of output for analysis.
	output "${config.analysisDir}/eval-results.csv"
	predictOutput "${config.analysisDir}/eval-preds.csv"
	userOutput "${config.analysisDir}/eval-user.csv"

	metric CoveragePredictMetric
	metric RMSEPredictMetric
	metric NDCGPredictMetric

	algorithm itemitem
	algorithm useruser
	algorithm extended
}
