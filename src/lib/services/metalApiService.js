// src/lib/services/metalApiService.js
const API_URL = 'https://tcpliage-backend.onrender.com/';
/**
 * Handles API interactions for the metal part designer
 */
export default {
  /**
   * Submit a design to the backend for quotation
   *
   * @param {Object} design - The metal part design specification
   * @returns {Promise} - Promise that resolves with the submission result
   */
  submitDesign: async (design) => {
    try {
      const response = await fetch(`${API_URL}/api/metal-piece/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(design),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "Error submitting design");
      }

      return await response.json();
    } catch (error) {
      console.error("API error:", error);
      throw error;
    }
  },

  /**
   * Get material options from the server
   *
   * @returns {Promise} - Promise that resolves with material options
   */
  getMaterials: async () => {
    try {
      const response = await fetch(`${API_URL}/api/materials-list/`)
      if (!response.ok) {
        throw new Error("Failed to fetch materials");
      }
      return await response.json();
    } catch (error) {
      console.error("API error:", error);
      // Fallback to mock data if server is not available
      return [
        {
          id: "steel",
          name: "Steel",
          description: "Strong and durable, good for structural applications",
          density: 7.85,
          maxThickness: 20,
          minThickness: 0.5,
          image: "/images/materials/steel.jpg",
        },
        // Other materials...
      ];
    }
  },

  /**
   * Get available finishes for a specific material
   *
   * @param {string} materialId - The material ID to get finishes for
   * @returns {Promise} - Promise that resolves with available finishes
   */
  getFinishes: async (materialId) => {
    try {
      const response = await fetch(
        `${API_URL}/api/finishes-for-material/?materialId=${materialId}`
      );
      if (!response.ok) {
        throw new Error("Failed to fetch finishes");
      }
      return await response.json();
    } catch (error) {
      console.error("API error:", error);
      // Fallback to mock data
      const commonFinishes = [
        {
          id: "none",
          name: "No Finish",
          description: "Raw metal without any coating or treatment",
        },
      ];

      // Add material-specific mock finishes
      return commonFinishes;
    }
  },
};
