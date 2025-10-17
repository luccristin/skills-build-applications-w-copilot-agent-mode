import React, { useEffect, useState } from 'react';

const Activities = () => {
  const [activities, setActivities] = useState([]);
  useEffect(() => {
    const endpoint = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/activities/`;
    fetch(endpoint)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setActivities(results);
      })
      .catch(err => {});
  }, []);
  return (
    <div className="card mb-4">
      <div className="card-body">
        <h2 className="card-title h4 mb-4">Activities</h2>
        <table className="table table-striped table-hover">
          <thead className="table-primary">
            <tr>
              <th>Name</th>
              <th>Duration (min)</th>
              <th>Calories</th>
            </tr>
          </thead>
          <tbody>
            {activities.map((activity, idx) => (
              <tr key={activity.id || idx}>
                <td>{activity.name || '-'}</td>
                <td>{activity.duration || '-'}</td>
                <td>{activity.calories || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <button className="btn btn-primary mt-3">Add Activity</button>
      </div>
    </div>
  );
};
export default Activities;
