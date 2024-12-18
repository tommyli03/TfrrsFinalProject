import React, { useState, useEffect } from "react";
import axios from "axios";
import 'bootstrap/dist/css/bootstrap.min.css';

const TopPerformers = () => {
  const [topPerformers, setTopPerformers] = useState([]);
  const [filteredYear, setFilteredYear] = useState('');
  const years = ['2024', '2023', '2022', '2021', '2020']; // Explicitly include these years

  useEffect(() => {
    const fetchTopPerformers = async () => {
      try {
        const url = filteredYear
          ? `http://localhost:5000/top_performers?year=${filteredYear}`
          : 'http://localhost:5000/top_performers';
        const response = await axios.get(url);
        setTopPerformers(response.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchTopPerformers();
  }, [filteredYear]);

  return (
    <div className="container mt-5">
      <h1 className="mb-4">Top 10 Performers at Each XC Nationals</h1>
      
      {/* Filter Dropdown */}
      <div className="mb-4">
        <label htmlFor="yearFilter" className="form-label">Filter by Year:</label>
        <select
          id="yearFilter"
          className="form-select"
          value={filteredYear}
          onChange={(e) => setFilteredYear(e.target.value)}
        >
          <option value="">All Years</option>
          {years.map((year, index) => (
            <option key={index} value={year}>{year}</option>
          ))}
        </select>
      </div>
      
      {/* Results Table */}
      <table className="table table-striped">
        <thead>
          <tr>
            <th>Year</th>
            <th>Place</th>
            <th>Name</th>
            <th>Team</th>
            <th>Time</th>
            <th>Avg Mile</th>
          </tr>
        </thead>
        <tbody>
          {topPerformers.map((performer, index) => (
            <tr key={index}>
              <td>{performer.race_year}</td>
              <td>{performer.place}</td>
              <td>{performer.athlete_name}</td>
              <td>{performer.team}</td>
              <td>{performer.time_str}</td>
              <td>{performer.avg_mile}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TopPerformers;
