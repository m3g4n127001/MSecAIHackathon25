import React, { useState } from 'react';
import IdentityTable from './components/IdentityTable';
import FilterSet from './components/FilterSet';
import ChatBox from './components/ChatBox';
import './App.css';

const App = () => {
    const [filters, setFilters] = useState({
        domain: 'Any',
        type: 'Any',
        source: 'Any',
        tags: 'Any',
        criticality: 'Any',
        accountStatus: 'Any',
    });

    const handleFilterChange = (filterName, value) => {
        setFilters((prevFilters) => ({
            ...prevFilters,
            [filterName]: value,
        }));
    };

    return (
        <div className="app-container">
            <div className="main-content">
            <h1 className="identity-table-heading">Identities Inventory</h1>
                <FilterSet filters={filters} onFilterChange={handleFilterChange} />
                <IdentityTable filters={filters} />
            </div>
            <div className="chatbox-container">
                <ChatBox />
            </div>
        </div>
    );
};

export default App;
