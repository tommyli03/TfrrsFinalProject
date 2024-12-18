import React, { useEffect, useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [topPerformers, setTopPerformers] = useState([]);

  useEffect(() => {
    // Fetch data from Flask backend
    axios.get('http://localhost:5000/top_performers')
      .then(response => setTopPerformers(response.data))
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
    <div className="container mt-5">
      <h1 className="mb-4">Top 10 Performers at XC Nationals in Last 5 Years</h1>
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
}

export default App;
