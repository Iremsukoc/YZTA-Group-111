import { useState, useEffect, useMemo } from 'react';
import { collection, query, where, onSnapshot, orderBy } from 'firebase/firestore';
import { db } from '../firebase.js';
import { useAuth } from '../context/AuthContext';

export function useFirestoreListener(collectionName, conditions = [], orderByField = null) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { currentUser } = useAuth();

  // Memoize the conditions array to prevent unnecessary re-renders
  const memoizedConditions = useMemo(() => {
    console.log('Memoizing conditions:', conditions);
    return conditions.map(condition => ({
      field: condition.field,
      operator: condition.operator,
      value: condition.value
    }));
  }, [conditions]);

  // Memoize the orderByField to prevent unnecessary re-renders
  const memoizedOrderByField = useMemo(() => {
    console.log('Memoizing orderByField:', orderByField);
    if (!orderByField) return null;
    return {
      field: orderByField.field,
      direction: orderByField.direction || 'desc'
    };
  }, [orderByField]);

  useEffect(() => {
    if (!currentUser) {
      setData([]);
      setLoading(false);
      return;
    }

    console.log("Firestore listener active");

    try {
      // Create query
      let q = collection(db, collectionName);
      
      // Add conditions
      memoizedConditions.forEach(condition => {
        q = query(q, where(condition.field, condition.operator, condition.value));
      });

      // Add ordering if specified
      if (memoizedOrderByField) {
        q = query(q, orderBy(memoizedOrderByField.field, memoizedOrderByField.direction));
      }

      // Set up real-time listener
      const unsubscribe = onSnapshot(
        q,
        (snapshot) => {
          const documents = [];
          snapshot.forEach((doc) => {
            const docData = {
              id: doc.id,
              assessment_id: doc.id,  // Add this for compatibility
              assessmentId: doc.id,   // Add this for camelCase compatibility
              ...doc.data()
            };
            documents.push(docData);
            
            // Debug logging for completed assessments
            if (docData.status === 'completed') {
              console.log('Firestore listener found completed assessment:', {
                id: docData.id,
                status: docData.status,
                imageAnalysisResult: docData.imageAnalysisResult,
                createdAt: docData.createdAt,
                updatedAt: docData.updatedAt
              });
            }
          });
          console.log('Firestore listener total documents:', documents.length);
          console.log('Firestore listener documents:', documents);
          setData(documents);
          setLoading(false);
          setError(null);

        },
        (err) => {
          console.error('Firestore listener error:', err);
          setError(err);
          setLoading(false);
        }
      );

      // Cleanup function
      return () => unsubscribe();
    } catch (err) {
      console.error('Error setting up Firestore listener:', err);
      setError(err);
      setLoading(false);
    }
  }, [currentUser, collectionName, memoizedConditions, memoizedOrderByField]);

  return { data, loading, error };
}

// Specific hook for assessments
export function useAssessmentsListener(status = null) {
  const { currentUser } = useAuth();
  
  // Memoize the conditions to prevent unnecessary re-renders
  const conditions = useMemo(() => {
    console.log('useAssessmentsListener - currentUser?.uid:', currentUser?.uid);
    const baseConditions = [
      { field: 'userId', operator: '==', value: currentUser?.uid }
    ];

    if (status === 'in_progress') {
      baseConditions.push({
        field: 'status',
        operator: 'in',
        value: [
          'general_test_in_progress',
          'triage_in_progress',
          'detailed_qa_in_progress',
          'awaiting_image'
        ]
      });
    } else if (status) {
      baseConditions.push({ field: 'status', operator: '==', value: status });
    }

    return baseConditions;
  }, [currentUser?.uid, status]);

  const orderByField = useMemo(() => ({
    field: 'updatedAt',
    direction: 'desc'
  }), []);

  return useFirestoreListener('assessments', conditions, orderByField);
} 