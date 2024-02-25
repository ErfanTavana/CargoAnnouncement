from goods_owner.serializers import Base_ModelSerializer
from carrier_owner.models import CarOwReqDriver, RoadFleet, CarOwReqGoodsOwner
from accounts.models import Driver, CarrierOwner, GoodsOwner
from goods_owner.models import InnerCargo, InternationalCargo, RequiredCarrier
from driver.models import DriverReqCarrierOwner
from goods_owner.models import GoodsOwnerReqCarOw


# اطلاعات قابل نمایش صاحب حمل کننده برای صاحب حمل کننده
class InfoCarrierOwnerForCarrierOwnerSerializers(Base_ModelSerializer):
    class Meta:
        model = CarrierOwner
        fields = '__all__'
        # Base_ModelSerializer.Meta.fields + (
        #     'id',
        #     'owner_full_name',
        # )


# اطلاعات قابل نمایش حمل کننده برای حمل کننده
class InfoRoadFleetForCarrierOwnerSerializers(Base_ModelSerializer):
    class Meta:
        model = RoadFleet
        fields = '__all__'
        # Base_ModelSerializer.Meta.fields + (
        #     'ownerType',
        #     'roomType',
        #     'vehichleType',
        #     'semiHeavyVehichle',
        #     'semiHeavyVehichleOthers',
        #     'HeavyVehichle',
        #     'heavy_vehicle_others',
        #     'plaque_one_num_check',
        #     'plaque_puller_num_check',
        #     'plaque_carriage_num_check',
        #     'plaque_container_num_check',
        #     'vehicle_card_bool',
        #     'vehicle_property_doc_bool',
        #     'vehicle_advocate_bool',
        #     'international_docs_bool',
        # )


# اطلاعات قابل نمایش راننده برای حمل کننده
class InfoDriverForCarrierOwnerSerializers(Base_ModelSerializer):
    class Meta:
        model = Driver
        fields = (
            'national_card_image_bool',
            'license_expiry_date',
            'smart_card_image_bool',
            'domestic_license',
            'international_license',
            'city',
            'province',
        )


# اطلاعات قابل نمایش درخواست همکاری صاحب حمل کننده به راننده برای حمل کننده
class InfoCarOwReqDriverForCarrierOwnerSerializers(Base_ModelSerializer):
    carrier_owner_full = InfoCarrierOwnerForCarrierOwnerSerializers(source='carrier_owner', read_only=True)
    carrier_full = InfoRoadFleetForCarrierOwnerSerializers(source='carrier', read_only=True)
    driver_full = InfoDriverForCarrierOwnerSerializers(source='driver', read_only=True)

    class Meta:
        model = CarOwReqDriver
        fields = Base_ModelSerializer.Meta.fields + (
            'user',
            'carrier_owner',
            'carrier_owner_full',
            'carrier',
            'carrier_full',
            'driver',
            'driver_full',
            'collaboration_type',
            'origin',
            'destination',
            'proposed_price',
            'request_result',
            'cancellation_time',
        )


# اطلاعات قابل نمایش صاحب بار برای حمل کننده
class InfoGoodsOwnerForCarrierOwnerSerializers(Base_ModelSerializer):
    class Meta:
        model = GoodsOwner
        fields = (
            'full_name',
        )


# اطلاعات قابل نمایش بار داخلی برای صاحب حمل کننده
class InfoInnerCargoForGoodsOwnerSerializers(Base_ModelSerializer):
    class Meta:
        model = InnerCargo
        fields = Base_ModelSerializer.Meta.fields + (
            'length',
            'width',
            'height',
            'cargoType',
            'pkgType',
            'description',
            'specialWidgets',
            'specialDesc',
            'sendersName',
            'senderMobileNum',
            'dischargeTimeDate',
            'duratio_ndischargeTime',
            'country',
            'delivery_provider_name',
            'delivery_provider_national_id',
            'delivery_provider_full_name',
            'delivery_provider_mobile',
            'cargo_receiver_name',
            'cargo_receiver_national_id',
            'cargo_receiver_full_name',
            'cargo_receiver_mobile',
            'state',
            'city',
            'street',
            'address',
            'customName',
            'deliveryTimeDate',
        )


# اطلاعات قابل نمایش بار خارجی برای صاحب بار

class InfoInternationalCargoForGoodsOwnerSerializers(Base_ModelSerializer):
    class Meta:
        model = InternationalCargo
        fields = Base_ModelSerializer.Meta.fields + (
            'length',
            'width',
            'height',
            'cargoType',
            'pkgType',
            'description',
            'specialWidgets',
            'storageBillNum',
            'storagePrice',
            'loadigPrice',
            'basculPrice',
            'specialDesc',
            'sendersName',
            'senderMobileNum',
            'dischargeTimeDate',
            'duratio_ndischargeTime',
            'country',
            'delivery_provider_name',
            'delivery_provider_national_id',
            'delivery_provider_full_name',
            'delivery_provider_mobile',
            'cargo_receiver_name',
            'cargo_receiver_national_id',
            'cargo_receiver_full_name',
            'cargo_receiver_mobile',
            'state',
            'city',
            'street',
            'address',
            'customName',
            'senderCountry',
            'senderState',
            'senderCity',
            'senderStreet',
            'senderAddress',
            'deliveryTimeDate',
            'dischargeTimeDate',
            'dischargeTime',
            'customNameEnd',
        )


# اطلاعات قابل نمایش حمل کننده های مورد نیاز برای صاحب بار
class InfoRequiredCarrierForGoodsOwnerSerializers(Base_ModelSerializer):
    inner_cargo_full = InfoInnerCargoForGoodsOwnerSerializers(source='inner_cargo', read_only=True)
    international_cargo_full = InfoInternationalCargoForGoodsOwnerSerializers(source='international_cargo',
                                                                              read_only=True)

    class Meta:
        model = RequiredCarrier
        fields = Base_ModelSerializer.Meta.fields + (
            'relinquished',
            'cargo_type',
            'inner_cargo',
            'inner_cargo_full',
            'international_cargo',
            'international_cargo_full',
            'cargo_weight',
            'counter',
            'room_type',
            'vehichle_type',
            'semi_heavy_vehichle',
            'semi_heavy_vehichle_others',
            'heavy_vehichle',
            'heavy_vehichle_others',
            'special_widget_carrier',
            'carrier_price',
            'cargo_price',
            'pallet_size',
            'pallet_size',
            'pallet_arrangement_type',
            'approximate_weight_per_packaging',
            'is_all_cargo_type',
            'approximate_weight_per_type',
            'specialized_lashing_required',
            'specialized_lashing_type_upload',
            'specialized_lashing_type_description',
            'need_warehouse',
            'warehouse_duration',
            'sender_additional_requests',
        )


class InfoCarOwReqGoodsOwnerForCarrierOwnerSerializers(Base_ModelSerializer):
    carrier_owner_full = InfoCarrierOwnerForCarrierOwnerSerializers(source='carrier_owner', read_only=True)
    road_fleet_full = InfoRoadFleetForCarrierOwnerSerializers(source='road_fleet', read_only=True)
    goods_owner_full = InfoGoodsOwnerForCarrierOwnerSerializers(source='goods_owner', read_only=True)
    required_carrier_full = InfoRequiredCarrierForGoodsOwnerSerializers(source='required_carrier', read_only=True)

    class Meta:
        model = CarOwReqGoodsOwner
        fields = Base_ModelSerializer.Meta.fields + (
            'user',
            'carrier_owner',
            'carrier_owner_full',
            'road_fleet',
            'road_fleet_full',
            'goods_owner',
            'goods_owner_full',
            'required_carrier',
            'required_carrier_full',
            'proposed_price',
            'request_result',
            'cancellation_time',
        )


# اطلاعات قابل نمایش درخواست همکاری راننده برای صاحب حمل کننده
class InfoDriverReqCarrierOwnerForCarrierOwnerSerializers(Base_ModelSerializer):
    carrier_owner_full = InfoCarrierOwnerForCarrierOwnerSerializers(source='carrier_owner', read_only=True)
    driver_full = InfoDriverForCarrierOwnerSerializers(source='driver', read_only=True)

    class Meta:
        model = DriverReqCarrierOwner
        fields = Base_ModelSerializer.Meta.fields + (
            'driver',
            'driver_full',
            'carrier_owner',
            'carrier_owner_full',
            'cargo_type',
            'proposed_price',
            'request_result',
            'cancellation_time',
            'source',
            'destination',
        )


class InfoGoodsOwnerReqCarOwForCarrierOwnerSerializers(Base_ModelSerializer):
    goods_owner_full = InfoGoodsOwnerForCarrierOwnerSerializers(source='goods_owner', read_only=True)
    carrier_owner_full = InfoCarrierOwnerForCarrierOwnerSerializers(source='carrier_owner', read_only=True)
    road_fleet_full = InfoRoadFleetForCarrierOwnerSerializers(source='road_fleet', read_only=True)
    #
    # # افزودن فیلد international_cargo_full به فهرست fields
    international_cargo_full = InfoInternationalCargoForGoodsOwnerSerializers(source='international_cargo',
                                                                              read_only=True)
    #
    inner_cargo_full = InfoInnerCargoForGoodsOwnerSerializers(source='inner_cargo', read_only=True)

    class Meta:
        model = GoodsOwnerReqCarOw
        fields = (
            'goods_owner',
            'goods_owner_full',
            'carrier_owner',
            'carrier_owner_full',
            'road_fleet',
            'road_fleet_full',
            'inner_cargo',
            'inner_cargo_full',
            'international_cargo',  # اطمینان حاصل شود که این فیلد در fields موجود است
            'international_cargo_full',
            'proposed_price',
            'request_result',
            'cancellation_time',
        )
