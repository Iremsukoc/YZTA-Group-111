import React from "react";
import { createPortal } from "react-dom";
import { ExclamationTriangleIcon } from "@heroicons/react/24/outline";

export default function DeleteConfirmModal({ isOpen, onClose, onConfirm }) {
  if (!isOpen) return null;

  return createPortal(
    <div
      style={{
        position: "fixed",
        inset: 0,
        backgroundColor: "rgba(0, 0, 0, 0.5)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 9999,
        fontFamily: "'Plus Jakarta Sans', sans-serif",
      }}
    >
      <div
        style={{
          background: "#fff",
          borderRadius: "16px",
          padding: "24px",
          maxWidth: "420px",
          width: "90%",
          boxShadow: "0 10px 40px rgba(0, 0, 0, 0.2)",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "12px",
            marginBottom: "16px",
          }}
        >
          <ExclamationTriangleIcon
            style={{ width: "28px", height: "28px", color: "#c0392b" }}
          />
          <h2
            style={{
              fontSize: "1rem",
              fontWeight: 600,
              color: "#c0392b",
            }}
          >
            Are you sure you want to delete your account?
          </h2>
        </div>
        <p style={{ fontSize: "0.875rem", color: "#374151", marginBottom: "20px" }}>
          This action is irreversible. Please proceed with caution.
        </p>
        <div
          style={{
            display: "flex",
            justifyContent: "flex-end",
            gap: "10px",
          }}
        >
          <button
            onClick={onClose}
            style={{
              padding: "8px 16px",
              borderRadius: "6px",
              backgroundColor: "#f3f4f6",
              border: "1px solid #d1d5db",
              color: "#374151",
              cursor: "pointer",
              fontWeight: 500,
            }}
          >
            Cancel
          </button>
          <button
            onClick={onConfirm}
            style={{
              padding: "8px 16px",
              borderRadius: "6px",
              backgroundColor: "#c0392b",
              color: "white",
              border: "none",
              cursor: "pointer",
              fontWeight: 500,
            }}
          >
            Yes, Delete
          </button>
        </div>
      </div>
    </div>,
    document.body
  );
}
