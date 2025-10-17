import React, { useEffect, useState } from 'react';

const Users = () => {
  const [users, setUsers] = useState([]);
  useEffect(() => {
    const endpoint = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/users/`;
    fetch(endpoint)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setUsers(results);
      })
      .catch(err => {});
  }, []);
  return (
    <div className="card mb-4">
      <div className="card-body">
        <h2 className="card-title h4 mb-4">Users</h2>
        <table className="table table-striped table-hover">
          <thead className="table-primary">
            <tr>
              <th>Name</th>
              <th>Email</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user, idx) => (
              <tr key={user.id || idx}>
                <td>{user.username || user.name || '-'}</td>
                <td>{user.email || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <button className="btn btn-primary mt-3">Add User</button>
      </div>
    </div>
  );
};
export default Users;
