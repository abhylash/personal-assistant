import React, { useState, useEffect } from 'react';
import { Plus, Trash2, Search, FileText, ArrowLeft, Check, X } from 'lucide-react';
import { knowledgeAPI } from '../services/api';

const KnowledgeManager = () => {
  const [documents, setDocuments] = useState([]);
  const [searchResults, setSearchResults] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [isAddingDocument, setIsAddingDocument] = useState(false);
  const [newDocument, setNewDocument] = useState({ title: '', content: '' });
  const [isLoading, setIsLoading] = useState(false);
  const [stats, setStats] = useState({});

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const statsData = await knowledgeAPI.getStats();
      setStats(statsData);
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setIsLoading(true);
    try {
      const results = await knowledgeAPI.searchDocuments(searchQuery);
      setSearchResults(results.results);
    } catch (error) {
      console.error('Error searching documents:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddDocument = async (e) => {
    e.preventDefault();
    if (!newDocument.content.trim()) return;

    setIsLoading(true);
    try {
      const response = await knowledgeAPI.addDocument(
        newDocument.content,
        newDocument.title || null
      );
      
      if (response.success) {
        setNewDocument({ title: '', content: '' });
        setIsAddingDocument(false);
        loadStats();
      }
    } catch (error) {
      console.error('Error adding document:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteDocument = async (documentId) => {
    if (!confirm('Are you sure you want to delete this document?')) return;

    setIsLoading(true);
    try {
      const response = await knowledgeAPI.deleteDocument(documentId);
      if (response.success) {
        loadStats();
        if (searchResults.length > 0) {
          handleSearch({ preventDefault: () => {} });
        }
      }
    } catch (error) {
      console.error('Error deleting document:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-blue-600 text-white p-4 shadow-lg">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <a href="/" className="flex items-center space-x-2 text-white hover:text-blue-200">
              <ArrowLeft className="w-5 h-5" />
              <span>Back to Chat</span>
            </a>
            <FileText className="w-8 h-8" />
            <h1 className="text-xl font-bold">Knowledge Management</h1>
          </div>
          <div className="text-sm">
            <span className="bg-blue-700 px-3 py-1 rounded-full">
              {stats.total_vectors || 0} documents
            </span>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto p-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          
          {/* Add Document Section */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-800">Add Document</h2>
              {!isAddingDocument && (
                <button
                  onClick={() => setIsAddingDocument(true)}
                  className="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  <Plus className="w-4 h-4" />
                  <span>Add Document</span>
                </button>
              )}
            </div>

            {isAddingDocument && (
              <form onSubmit={handleAddDocument} className="space-y-4">
                <div>
                  <input
                    type="text"
                    placeholder="Document title (optional)"
                    value={newDocument.title}
                    onChange={(e) => setNewDocument({ ...newDocument, title: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <textarea
                    placeholder="Document content..."
                    value={newDocument.content}
                    onChange={(e) => setNewDocument({ ...newDocument, content: e.target.value })}
                    rows={8}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                <div className="flex space-x-2">
                  <button
                    type="submit"
                    disabled={isLoading || !newDocument.content.trim()}
                    className="flex items-center space-x-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 disabled:bg-gray-300 transition-colors"
                  >
                    <Check className="w-4 h-4" />
                    <span>Save</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setIsAddingDocument(false);
                      setNewDocument({ title: '', content: '' });
                    }}
                    className="flex items-center space-x-2 bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors"
                  >
                    <X className="w-4 h-4" />
                    <span>Cancel</span>
                  </button>
                </div>
              </form>
            )}
          </div>

          {/* Search Section */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Search Documents</h2>
            <form onSubmit={handleSearch} className="space-y-4">
              <div className="flex space-x-2">
                <input
                  type="text"
                  placeholder="Search knowledge base..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                  type="submit"
                  disabled={isLoading || !searchQuery.trim()}
                  className="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-300 transition-colors"
                >
                  <Search className="w-4 h-4" />
                  <span>Search</span>
                </button>
              </div>
            </form>

            {/* Search Results */}
            {searchResults.length > 0 && (
              <div className="mt-4 space-y-3">
                <h3 className="font-medium text-gray-700">Results ({searchResults.length})</h3>
                {searchResults.map((result, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-3">
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="font-medium text-gray-800">
                        {result.metadata?.title || 'Untitled Document'}
                      </h4>
                      <div className="flex items-center space-x-2">
                        <span className="text-xs text-gray-500">
                          Score: {(result.score * 100).toFixed(1)}%
                        </span>
                        <button
                          onClick={() => handleDeleteDocument(result.metadata?.document_id)}
                          className="text-red-600 hover:text-red-800"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                    <p className="text-sm text-gray-600 line-clamp-3">
                      {result.content}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default KnowledgeManager;
