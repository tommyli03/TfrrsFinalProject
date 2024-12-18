// src/XCNationalsResults.js
import React, { useState, useEffect } from "react";
import axios from "axios";
import 'bootstrap/dist/css/bootstrap.min.css';

const XCNationalsResults = () => {
  const [results, setResults] = useState([]);
  const [selectedYear, setSelectedYear] = useState('');
  const years = ['None', '2024', '2023', '2022', '2021', '2020']; // Add "None" option

  useEffect(() => {
    const fetchResults = async () => {
      if (selectedYear && selectedYear !== 'None') {
        try {
          const response = await axios.get(`http://localhost:5000/xc_nationals_results?year=${selectedYear}`);
          setResults(response.data);
        } catch (error) {
          console.error("Error fetching XC Nationals Results:", error);
        }
      } else {
        setResults([]); // Clear results if "None" is selected
      }
    };

    fetchResults();
  }, [selectedYear]);

  return (
    <div className="container mt-5">
      <h1 className="mb-4">XC Nationals Results</h1>
      
      {/* Filter Dropdown */}
      <div className="mb-4">
        <label htmlFor="yearFilter" className="form-label">Filter by Year:</label>
        <select
          id="yearFilter"
          className="form-select"
          value={selectedYear}
          onChange={(e) => setSelectedYear(e.target.value)}
        >
          <option value="">Select a Year</option>
          {years.map((year, index) => (
            <option key={index} value={year}>{year}</option>
          ))}
        </select>
      </div>
      
      {/* Results Table */}
      {results.length > 0 && (
        <table className="table table-striped">
          <thead>
            <tr>
              <th>Year</th>
              <th>Place</th>
              <th>Name</th>
              <th>Year</th>
              <th>Team</th>
              <th>Avg Mile</th>
              <th>Time</th>
              <th>Score</th>
            </tr>
          </thead>
          <tbody>
            {results.map((result, index) => (
              <tr key={index}>
                <td>{result.race_year}</td>
                <td>{result.place}</td>
                <td>{result.athlete_name}</td>
                <td>{result.athlete_year}</td>
                <td>{result.team}</td>
                <td>{result.avg_mile}</td>
                <td>{result.time_str}</td>
                <td>{result.score}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default XCNationalsResults;
