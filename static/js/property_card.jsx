'use strict';
import React from "react";

function PropertyCard({ property }) {
  const [isFavorite, setIsFavorite] = React.useState(property.isFavorite);

  function handleSubmit(event) {
    event.preventDefault();
    setIsFavorite(prevState => !prevState); // updater function form 

    // Submit the form using AJAX
    const xhr = new XMLHttpRequest();
    xhr.open("POST", `/properties/${property.zpid}/favorite`);
    xhr.send();
  }

  return (
    <div className="card ">
      <div className="absolute top-2.5 right-2.5 text-3xl">
        <form onSubmit={handleSubmit}>
          <button type="submit">
            <i className={isFavorite ? "fa-solid fa-heart" : "fa-regular fa-heart"}></i>
          </button>
        </form>
      </div>
      <div className='card_image'>
        <a href={`/properties/${property.zpid}`}>
          <img src={property.img_src} alt="Home" />
        </a>
      </div>
      <div className='card_info my-2 mx-2'>
        <p className="text-xl font-semibold">${property.price}</p>
        <p>
          <strong>{property.bedrooms}</strong> bds |
          <strong>{property.bathrooms}</strong> ba |
          <strong>{property.lot_area_value }</strong> {property.lot_area_unit}
        </p>
        <p>{property.address}</p>
      </div>
    </div> 
  );
}

export default PropertyCard;
