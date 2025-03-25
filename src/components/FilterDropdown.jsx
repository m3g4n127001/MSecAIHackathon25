import React from 'react';
import './FilterDropdown.css';

const FilterDropdown = ({ filterName, options, selectedValue, onChange }) => {
    return (
        <div className="filter-dropdown">
            <h4>{filterName}</h4>
            {options.map((option) => (
                <label key={option} className="dropdown-item">
                    <input
                        type="checkbox"
                        checked={selectedValue === option}
                        onChange={() => onChange(option)}
                    />
                    {option}
                </label>
            ))}
            <button className="apply-button" onClick={() => onChange(selectedValue)}>
                Apply
            </button>
        </div>
    );
};

export default FilterDropdown;
