<template>
  <div class="flex-grow-1 d-flex flex-column">
    <div class="app container-fluid d-flex flex-grow-1">
      <div class="row no-gutters flex-grow-1">
        <div class="col-sm left-column">
          <div class="map-with-stats d-flex flex-column">
            <dtp-map
              :center="center"
              :mvcs="mvcs"
              :handleMounted="updateData"
              :handleZoomEnd="updateData"
              :handleZoomStart="cancelRequest"
            ></dtp-map>
            <dtp-brief
              :dead="brief.dead"
              :deadAuto="brief.deadAuto"
              :deadBicycle="brief.deadBicycle"
              :deadPedestrian="brief.deadPedestrian"
              :injured="brief.injured"
              :injuredAuto="brief.injuredAuto"
              :injuredBicycle="brief.injuredBicycle"
              :injuredPedestrian="brief.injuredPedestrian"
              :mvcCount="brief.mvcCount"
              ref="brief"
            ></dtp-brief>
          </div>
        </div>
        <div class="col-xl-2 col-lg-3 col-md-4 col-sm-5 right-column"></div>
      </div>
    </div>
  </div>
</template>



  


<script lang="ts" src='./DTPArea.ts'></script>