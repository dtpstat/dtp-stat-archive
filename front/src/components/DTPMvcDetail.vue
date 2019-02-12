<template>
  <div class="mvc-details">
    <button aria-label="Close" class="close" onClick="{this.props.onCloseMvc}" type="button">
      <span aria-hidden="true">&times;</span>
    </button>

    <h4>{date.format('DD.MM.YYYY')}</h4>

    <h5>{getMvcTypeName(mvc, dictionaries)}</h5>

    <p>Пострадали - {mvc.injured}, погибли - {mvc.dead}</p>

    <div>
      <p class="list-header">Нарушения:</p>

      <ul class="offence-list list-unstyled">{participantsWithOffences.map((po, index) => (
        <li class="media align-items-center" key="{index}">
          <i class="mr-3 fa" aria-hidden="true"/>
          <div class="media-body">{po.offenceName}</div>
        </li>))}
      </ul>
    </div>

    <div class="text-center">
      <a class="more-link btn btn-outline-dark" href="/dtp/" target="_blank">Подробнее</a>
    </div>
  </div>
</template>
        