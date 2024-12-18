import React from "react";
import TopPerformers from "./TopPerformers";
import XCNationalsResults from "./XCNationalsResults";
import TeamRankings from "./TeamRankings";
import FiveKAnalysis from "./FiveKAnalysis";

const HomePage = () => {
  return (
    <div>
        <XCNationalsResults />
        <TopPerformers />
        <TeamRankings />
        <FiveKAnalysis />
    </div>
  );
};

export default HomePage;
