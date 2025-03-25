import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './IdentityTable.css';

const IdentityTable = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get('/identities.csv');
                const csvData = response.data;
                const rows = csvData
                    .split('\n')
                    .map(row => row.split(',').map(cell => cell.trim()));

                const headers = rows[0];
                const parsedData = rows.slice(1).map(row => {
                    return headers.reduce((acc, header, index) => {
                        acc[header] = row[index] || 'NA'; // Fallback for missing data
                        return acc;
                    }, {});
                });

                //console.log('Parsed Data:', parsedData); // Debugging
                setData(parsedData);
            } catch (error) {
                console.error('Error fetching CSV data:', error);
                setData([]);
            }
        };

        fetchData();
    }, []);

    return (
        <div className="identity-table-container">
            <div className="table-wrapper">
                {data.length > 0 ? (
                    <table className="identity-table">
                        <thead>
                            <tr>
                                {Object.keys(data[0]).map((key) => (
                                    <th key={key}>{key}</th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {data.map((row, index) => (
                                <tr key={index}>
                                    {Object.values(row).map((value, i) => (
                                        <td key={i}>{value}</td>
                                    ))}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                ) : (
                    <p className="no-data-msg">No data available. Please check the CSV file.</p>
                )}
            </div>
        </div>
    );
};

export default IdentityTable;
