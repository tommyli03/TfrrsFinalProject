import React, { useState, useEffect } from "react";
import axios from "axios";

const TeamRankings = () => {
    const [teamRankings, setTeamRankings] = useState([]);
    const [selectedYear, setSelectedYear] = useState("None");

    useEffect(() => {
        if (selectedYear === "None") {
            setTeamRankings([]);
            return;
        }

        axios.get(`http://localhost:5000/team_rankings?year=${selectedYear}`)
            .then(response => setTeamRankings(response.data))
            .catch(error => console.error("Error fetching team rankings:", error));
    }, [selectedYear]);

    return (
        <div className="container mt-5">
            <h1 className="mb-4">Cross Country Team Rankings</h1>
            <div className="mb-3">
                <label htmlFor="yearSelect" className="form-label">Select a Year:</label>
                <select
                    id="yearSelect"
                    className="form-select"
                    value={selectedYear}
                    onChange={e => setSelectedYear(e.target.value)}
                >
                    <option value="None">None</option>
                    <option value="2024">2024</option>
                    <option value="2023">2023</option>
                    <option value="2022">2022</option>
                    <option value="2021">2021</option>
                </select>
            </div>
            {teamRankings.length > 0 ? (
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>Year</th>
                            <th>Team</th>
                            <th>Total Score</th>
                            <th>Team Rank</th>
                        </tr>
                    </thead>
                    <tbody>
                        {teamRankings.map((team, index) => (
                            <tr key={index}>
                                <td>{team.race_year}</td>
                                <td>{team.team}</td>
                                <td>{team.total_score}</td>
                                <td>{team.team_rank}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            ) : (
                <p>Select a year to view team rankings.</p>
            )}
        </div>
    );
};

export default TeamRankings;
