import React, { useState } from 'react';
import FilterDropdown from './FilterDropdown';
import './FilterSet.css';

const FilterSet = () => {
    const [activeFilter, setActiveFilter] = useState(null);
    const [filters, setFilters] = useState({
        Domain: 'Any',
        Type: 'Any',
        Source: 'Any',
        Tags: 'Any',
        CriticalityLevel: 'Any',
        AccountStatus: 'Any',
    });

    const handleFilterClick = (filterName) => {
        setActiveFilter(activeFilter === filterName ? null : filterName);
    };

    const handleFilterChange = (filterName, value) => {
        setFilters({ ...filters, [filterName]: value });
        setActiveFilter(null);
    };

    const filterOptions = {
        Domain: ["domain1.test.local", "domain2.test.local", "MCASAATP.ccsctp.net", "mcasaatp.ccsctp.net", "darya3112.test.local", "vs.test.local", "domain3.test.local", "domain5.test.local", "yuvalp.test1025.local", "mydomain14.com", "yuval22.test.local", "dev-93500790.okta.com", "darya1.test.local", "barbox1.test.local", "domain8.test.local", "darya2.test.local", "yuval30.test.local", "efig3.devlab.test", "altshuler.xyz"],
        Type: ["User", "Service"],
        Source: ["On-premises", "Cloud", "Hybrid"],
        Tags: ["Sensitive", "Honeytoken"],
        CriticalityLevel: ["Very High", "High", "Medium", "Low", "None"],
        AccountStatus: ["Enabled", "Disabled"]
    };

    return (
        <div className="filter-set">
            {Object.keys(filters).map((filterName) => (
                <div key={filterName} className="filter-item">
                    <button
                        className={`filter-button ${activeFilter === filterName ? 'active' : ''}`}
                        onClick={() => handleFilterClick(filterName)}
                    >
                        {`${filterName}: ${filters[filterName]}`}
                    </button>
                    {activeFilter === filterName && (
                        <FilterDropdown
                            filterName={filterName}
                            options={filterOptions[filterName]}
                            selectedValue={filters[filterName]}
                            onChange={(value) => handleFilterChange(filterName, value)}
                        />
                    )}
                </div>
            ))}
        </div>
    );
};

export default FilterSet;
