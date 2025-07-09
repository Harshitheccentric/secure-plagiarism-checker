prj/secure-plagiarism-checker/frontend/src/components/ReportDisplay.js
import React, { useState } from 'react';
import { saveMatchedSequences } from '../apiService';

const ReportDisplay = ({ reportData }) => {
  const [savingMatches, setSavingMatches] = useState({});

  const handleSaveMatches = async (comparison) => {
    const key = `${comparison.file1}_${comparison.file2}`;
    setSavingMatches(prev => ({ ...prev, [key]: true }));

    try {
      const matchData = {
        file1: comparison.file1,
        file2: comparison.file2,
        matched_sequences: comparison.matched_sequences || [],
        similarity: comparison.similarity,
        method: comparison.method
      };

      const result = await saveMatchedSequences(matchData);
      
      alert(`✅ Matched sequences saved successfully!\nFile: ${result.filename}\nTotal matches: ${result.total_matches}`);
      
    } catch (error) {
      console.error('Error saving matches:', error);
      alert('❌ Failed to save matched sequences. Please try again.');
    } finally {
      setSavingMatches(prev => ({ ...prev, [key]: false }));
    }
  };

  const renderMatchedSequences = (sequences) => {
    if (!sequences || sequences.length === 0) {
      return <p className="text-gray-500 text-sm">No matched sequences available</p>;
    }

    return (
      <div className="mt-2">
        <h4 className="font-medium text-sm mb-2">Matched Sequences:</h4>
        <div className="max-h-40 overflow-y-auto space-y-1">
          {sequences.slice(0, 5).map((match, idx) => (
            <div key={idx} className="bg-yellow-50 p-2 rounded text-xs">
              <span className="font-medium text-blue-600">[{match.type}]</span>
              <span className="ml-2 text-gray-700">"{match.content}"</span>
              <span className="ml-2 text-gray-500">({match.length} {match.type === 'common_word' ? 'word' : 'words'})</span>
            </div>
          ))}
          {sequences.length > 5 && (
            <p className="text-xs text-gray-500">... and {sequences.length - 5} more sequences</p>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-4">
      {reportData.comparisons.map((comparison, index) => {
        const key = `${comparison.file1}_${comparison.file2}`;
        const isLoading = savingMatches[key];
        
        return (
          <div key={index} className="border rounded-lg p-4 bg-white shadow-sm">
            <div className="flex justify-between items-start mb-3">
              <div>
                <h3 className="font-semibold text-lg">
                  {comparison.file1} vs {comparison.file2}
                </h3>
                <div className="flex items-center space-x-4 mt-1">
                  <span className={`px-2 py-1 rounded text-sm font-medium ${
                    comparison.similarity >= 80 ? 'bg-red-100 text-red-800' :
                    comparison.similarity >= 50 ? 'bg-yellow-100 text-yellow-800' :
                    comparison.similarity >= 20 ? 'bg-blue-100 text-blue-800' :
                    'bg-green-100 text-green-800'
                  }`}>
                    {comparison.similarity}% similarity
                  </span>
                  <span className="text-sm text-gray-600">
                    {comparison.common_segments} segments
                  </span>
                  <span className="text-sm text-gray-500">
                    Method: {comparison.method}
                  </span>
                </div>
              </div>
              
              <button
                onClick={() => handleSaveMatches(comparison)}
                disabled={isLoading || !comparison.matched_sequences || comparison.matched_sequences.length === 0}
                className={`px-4 py-2 rounded text-sm font-medium transition-colors ${
                  isLoading 
                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    : comparison.matched_sequences && comparison.matched_sequences.length > 0
                      ? 'bg-blue-600 text-white hover:bg-blue-700'
                      : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                }`}
              >
                {isLoading ? 'Saving...' : 'Save Matches'}
              </button>
            </div>
            
            {renderMatchedSequences(comparison.matched_sequences)}
          </div>
        );
      })}
    </div>
  );
};

export default ReportDisplay;