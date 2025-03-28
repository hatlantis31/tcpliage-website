// src/lib/services/metalApiService.js

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
        const response = await fetch('/api/metal-piece', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(design)
        });
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.message || 'Error submitting design');
        }
        
        return await response.json();
      } catch (error) {
        console.error('API error:', error);
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
        // In production, this would be an API call
        // For now, return mock data
        return [
          { 
            id: 'steel', 
            name: 'Steel', 
            description: 'Strong and durable, good for structural applications',
            density: 7.85, // g/cm³
            maxThickness: 20,
            minThickness: 0.5,
            image: '/images/materials/steel.jpg'
          },
          { 
            id: 'aluminum', 
            name: 'Aluminum', 
            description: 'Lightweight and corrosion-resistant',
            density: 2.7,
            maxThickness: 15,
            minThickness: 0.5,
            image: '/images/materials/aluminum.jpg'
          },
          { 
            id: 'copper', 
            name: 'Copper', 
            description: 'Excellent electrical and thermal conductivity',
            density: 8.96,
            maxThickness: 10,
            minThickness: 0.5,
            image: '/images/materials/copper.jpg'
          },
          { 
            id: 'brass', 
            name: 'Brass', 
            description: 'Good machinability and corrosion resistance',
            density: 8.4,
            maxThickness: 10,
            minThickness: 0.5,
            image: '/images/materials/brass.jpg'
          }
        ];
      } catch (error) {
        console.error('API error:', error);
        throw error;
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
        // In production, this would be an API call
        // For now, return mock data based on the material
        
        // Common finishes for all materials
        const commonFinishes = [
          { 
            id: 'none', 
            name: 'No Finish', 
            description: 'Raw metal without any coating or treatment'
          }
        ];
        
        // Material-specific finishes
        const materialFinishes = {
          'steel': [
            { 
              id: 'painted', 
              name: 'Painted', 
              description: 'Decorative and protective coating available in various colors'
            },
            { 
              id: 'powder-coated', 
              name: 'Powder Coated', 
              description: 'Durable finish that is more resistant than conventional paint'
            },
            { 
              id: 'galvanized', 
              name: 'Galvanized', 
              description: 'Zinc coating that prevents corrosion'
            }
          ],
          'aluminum': [
            { 
              id: 'painted', 
              name: 'Painted', 
              description: 'Decorative and protective coating available in various colors'
            },
            { 
              id: 'powder-coated', 
              name: 'Powder Coated', 
              description: 'Durable finish that is more resistant than conventional paint'
            },
            { 
              id: 'anodized', 
              name: 'Anodized', 
              description: 'Electrochemical process that increases corrosion resistance'
            },
            { 
              id: 'brushed', 
              name: 'Brushed', 
              description: 'Satin finish with fine lines'
            },
            { 
              id: 'polished', 
              name: 'Polished', 
              description: 'Smooth, reflective surface'
            }
          ],
          'copper': [
            { 
              id: 'brushed', 
              name: 'Brushed', 
              description: 'Satin finish with fine lines'
            },
            { 
              id: 'polished', 
              name: 'Polished', 
              description: 'Smooth, reflective surface'
            }
          ],
          'brass': [
            { 
              id: 'brushed', 
              name: 'Brushed', 
              description: 'Satin finish with fine lines'
            },
            { 
              id: 'polished', 
              name: 'Polished', 
              description: 'Smooth, reflective surface'
            }
          ]
        };
        
        return [
          ...commonFinishes,
          ...(materialFinishes[materialId] || [])
        ];
      } catch (error) {
        console.error('API error:', error);
        throw error;
      }
    }
  };